# Study plan

One track per weekday. Each track starts from the basics and builds up, one lesson a day.
The routine teaches the first lesson in today's track that `scripts/study_history.py`
doesn't list yet. A lesson that's too big for one day can be split into "part 1" and
"part 2" on consecutive weeks. When a track is finished, the routine goes deeper on its
earlier lessons (a harder angle, a real XLIO or NVIDIA case, a hands-on measurement),
still without repeating a covered topic.

Edit this file to change what you learn. Lessons can be reordered, added or removed.

## Sunday: XLIO and kernel bypass
1. What a socket is, and what really happens when an app calls send() and recv()
2. Where the time goes in the normal Linux network path: system calls, copies, interrupts, context switches
3. What a network card does: packet rings, descriptors and DMA
4. Kernel bypass: the idea, what you gain and what you give up
5. LD_PRELOAD: how XLIO slips under an unmodified app
6. Interrupts vs polling, and busy-polling
7. A TCP/IP stack in user space: the jobs XLIO takes over from the kernel
8. Zero-copy send and receive
9. Offloads: checksum, TSO, LRO and GRO
10. Striding receive queues: catching many small packets efficiently
11. TLS and NVMe/TCP offload
12. XLIO vs DPDK vs AF_XDP vs io_uring: when to use which

## Monday: RDMA and network cards
1. What RDMA is, and how one machine writes into another's memory without its CPU
2. Memory registration: why the card needs pinned, registered memory
3. Queue pairs, work requests and doorbells
4. Completion queues: how the card says the work is done
5. Two-sided vs one-sided: send/receive vs RDMA read, write and atomics
6. Transport types: RC, UC, UD and DC
7. InfiniBand vs RoCEv2 (RDMA over Ethernet)
8. Lossless Ethernet: PFC, ECN and DCQCN
9. Inside a ConnectX card: what the hardware does for you
10. SR-IOV: one physical card, many virtual cards
11. GPUDirect RDMA: network straight into GPU memory
12. BlueField DPU: a computer on the network card

## Tuesday: TCP in depth
1. What TCP promises: a reliable, ordered byte stream, and the three-way handshake
2. Sequence numbers, ACKs and retransmission
3. Flow control and the receive window
4. The congestion window and slow start
5. Congestion avoidance, packet loss and CUBIC
6. Fast retransmit and SACK
7. Nagle's algorithm and delayed ACK: the small-message latency trap
8. Closing connections and TIME_WAIT
9. BBR: congestion control from bandwidth and round-trip time
10. Data center TCP: ECN, DCTCP and incast
11. The Linux receive path: interrupt, NAPI, skb, socket
12. Spreading packets across cores: RSS, RPS and XPS

## Wednesday: computer architecture and performance
1. Latency vs throughput, and how to measure each one
2. The memory hierarchy: registers, caches, DRAM, and why distance costs time
3. Cache lines, false sharing and cache coherence
4. NUMA: why it matters which CPU socket your memory and NIC are on
5. Virtual memory, the TLB and hugepages
6. PCIe: how a device talks to the CPU and memory
7. Interrupts, IRQ affinity and CPU pinning
8. Tail latency: why p99 matters more than the average
9. Finding hot spots with perf and flame graphs
10. eBPF: small, safe programs inside the kernel
11. SIMD: one instruction, many data items
12. The roofline model: is your code limited by compute or by memory?
13. Benchmarking networks: sockperf, iperf and perftest

## Thursday: AI compute and interconnect
1. Why AI runs on GPUs: matrix math and massive parallelism
2. GPU memory: HBM, and why memory bandwidth is often the limit
3. How training works at a glance: forward pass, backward pass, gradients
4. Data parallelism and all-reduce: keeping many GPUs in sync
5. NCCL collectives: ring vs tree all-reduce
6. NVLink and NVSwitch: fast GPU-to-GPU links inside a server or rack
7. NVL72: a whole rack working like one giant GPU
8. Scale-out networking between racks: InfiniBand and Spectrum-X
9. SHARP: doing the math inside the switch
10. Tensor and pipeline parallelism: splitting one model across GPUs
11. Expert parallelism and mixture-of-experts models
12. GPUDirect Storage: from disk to GPU without the CPU

## Friday: AI inference
1. What happens when you send a prompt: tokens, prefill and decode
2. The KV cache: what it stores and why it grows with every token
3. Batching and continuous batching: serving many users at once
4. PagedAttention and vLLM: managing KV-cache memory like an OS manages pages
5. Quantization: smaller numbers, faster and cheaper models
6. Speculative decoding: guessing ahead to go faster
7. Prefill/decode disaggregation: splitting the two phases across machines
8. Moving KV cache over the network: NIXL
9. Serving software: TensorRT-LLM, vLLM and Triton
10. Dynamo: running inference at data center scale
11. Measuring inference: time to first token, tokens per second, cost per token

## Saturday: AI agents and sandboxes
1. What an AI agent is: the loop of think, act, observe
2. Tool calling: how a model uses tools
3. MCP: a standard plug for connecting tools and data to models
4. Context windows and memory: what the model can "see"
5. Planning, multi-step tasks and subagents
6. Evals: how to tell whether an agent is any good
7. Why agents need sandboxes
8. Containers: namespaces and cgroups
9. gVisor: a kernel in user space as a safety layer
10. Firecracker microVMs: tiny virtual machines that start fast
11. Prompt injection, and how to defend against it
