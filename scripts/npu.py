# Benchmark CPU vs Snapdragon NPU (QNN) inference.

import json
import sys
import time
from pathlib import Path

SAMPLE = sys.argv[1] if len(sys.argv) > 1 else "sample.wav"
results = {"sample": SAMPLE, "cpu": None, "npu": None}


def bench_whisper_cpu(audio_path):
    #transcribe a file with faster-whisper on CPU (int8).
    from faster_whisper import WhisperModel
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    t0 = time.time()
    segments, info = model.transcribe(audio_path)
    text = " ".join(s.text for s in segments)
    dt = time.time() - t0
    return {
        "engine": "faster-whisper (CPU, int8)",
        "seconds": round(dt, 2),
        "rtf": round(dt / max(info.duration, 0.01), 3),
        "words_per_sec": round(len(text.split()) / max(dt, 0.01), 1),
    }


def bench_matmul(ep):
    # Synthetic NPU probe: same ONNX matmul, CPU vs QNN execution provider.
    import numpy as np
    import onnxruntime
    from onnxruntime import helper, TensorProto
    import onnxruntime as ort

    n = 512
    node = helper.make_node("MatMul", ["a", "b"], ["c"])
    graph = helper.make_graph(
        [node], "g",
        [helper.make_tensor_value_info("a", TensorProto.FLOAT, [n, n]),
         helper.make_tensor_value_info("b", TensorProto.FLOAT, [n, n])],
        [helper.make_tensor_value_info("c", TensorProto.FLOAT, [n, n])],
    )
    model = helper.make_model(graph)
    onnxruntime.checker.check_model(model)
    sess = ort.InferenceSession(model.SerializeToString(),
                                providers=[ep, "CPUExecutionProvider"])
    a = np.random.randn(n, n).astype(np.float32)
    b = np.random.randn(n, n).astype(np.float32)
    t0 = time.time()
    for _ in range(50):
        sess.run(None, {"a": a, "b": b})
    return round((time.time() - t0) / 50 * 1000, 2)  # ms per run


def bench_npu():
    import onnxruntime as ort
    avail = ort.get_available_providers()
    if "QNNExecutionProvider" not in avail:
        return {"error": "QNN EP not found. Install onnxruntime-qnn + Qualcomm AI Hub model."}
    cpu_ms = bench_matmul("CPUExecutionProvider")
    npu_ms = bench_matmul("QNNExecutionProvider")
    return {
        "engine": "ONNX Runtime QNN (Snapdragon NPU)",
        "matmul_512_ms_cpu": cpu_ms,
        "matmul_512_ms_npu": npu_ms,
        "speedup_x": round(cpu_ms / max(npu_ms, 0.01), 2),
        "providers": avail,
    }


if Path(SAMPLE).exists():
    results["cpu"] = bench_whisper_cpu(SAMPLE)
    print("CPU:", results["cpu"])
else:
    print("Sample audio not found - skipping Whisper bench (CPU).")

try:
    results["npu"] = bench_npu()
    print("NPU:", results["npu"])
except Exception as e:
    results["npu"] = {"error": str(e)}
    print("NPU bench failed (expected on non-Snapdragon machines):", e)

Path("benchmark_results.json").write_text(json.dumps(results, indent=2))
print("Saved -> benchmark_results.json")