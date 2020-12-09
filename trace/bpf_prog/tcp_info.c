#include <uapi/linux/ptrace.h>
#include <net/sock.h>
#include <bcc/proto.h>
#include <linux/nsproxy.h>
#include <linux/fs.h>
#include <linux/ns_common.h>
#include <linux/utsname.h>
#include <linux/pid_namespace.h>

struct ipv4_data_t {
    u64 ts_us;
    u32 pid;
    u32 saddr;
    u32 daddr;
    u8 ip;
    u16 lport;
    u16 dport;
    // u32 oldstate;
    // u32 newstate;
    u32 state;
    char task[TASK_COMM_LEN];
    u32 net_ns;
};
BPF_PERF_OUTPUT(ipv4_events);

struct ipv6_data_t {
    u64 ts_us;
    u32 pid;
    unsigned __int128 saddr;
    unsigned __int128 daddr;
    u8 ip;
    u16 lport;
    u16 dport;
    // u32 oldstate;
    // u32 newstate;
    u32 state;
    char task[TASK_COMM_LEN];
    u32 net_ns;
};
BPF_PERF_OUTPUT(ipv6_events);

// int kretprobe__inet_sock_set_state(struct pt_regs *ctx) {
// TRACEPOINT_PROBE(sock, inet_sock_set_state) {
//     if (args->protocol != IPPROTO_TCP)
//         return 0;
//     u32 pid = bpf_get_current_pid_tgid() >> 32;
//     // sk is used as a UUID
//     struct sock *sk = (struct sock *)args->skaddr;
//     // lport is either used in a filter here, or later
//     u16 lport = args->sport;
//     // dport is either used in a filter here, or later
//     u16 dport = args->dport;
    
//     // netns
//     struct task_struct *task;
//     task = (struct task_struct *)bpf_get_current_task();

//     char *ns_name = (char *)task->nsproxy->net_ns->ns.ops->;


//     if (args->family == AF_INET) {
//         struct ipv4_data_t data4 = {
//             .oldstate = args->oldstate,
//             .newstate = args->newstate,
//             .ip = 4 };
//         data4.ts_us = bpf_ktime_get_ns() / 1000;
//         __builtin_memcpy(&data4.saddr, args->saddr, sizeof(data4.saddr));
//         __builtin_memcpy(&data4.daddr, args->daddr, sizeof(data4.daddr));
//         // a workaround until data4 compiles with separate lport/dport
//         data4.lport = lport;
//         data4.dport = dport;
//         data4.pid = pid;
//         data4.net_ns = ns_name;
//         bpf_get_current_comm(&data4.task, sizeof(data4.task));
//         ipv4_events.perf_submit(args, &data4, sizeof(data4));
//     } else /* 6 */ {
//         struct ipv6_data_t data6 = {
//             .oldstate = args->oldstate,
//             .newstate = args->newstate,
//             .ip = 4 };
//         data6.ts_us = bpf_ktime_get_ns() / 1000;
//         __builtin_memcpy(&data6.saddr, args->saddr_v6, sizeof(data6.saddr));
//         __builtin_memcpy(&data6.daddr, args->daddr_v6, sizeof(data6.daddr));
//         // a workaround until data6 compiles with separate lport/dport
//         data6.lport = lport;
//         data6.dport = dport;
//         data6.pid = pid;
//         data6.net_ns = ns_name;
//         bpf_get_current_comm(&data6.task, sizeof(data6.task));
//         ipv6_events.perf_submit(args, &data6, sizeof(data6));
//     }


//     return 0;
// }

// int trace__inet_sock_set_state(struct pt_regs *ctx) {
TRACEPOINT_PROBE(sock, inet_sock_set_state) {
    // struct sock *newsk = (struct sock *)PT_REGS_RC(ctx);
    struct sock *newsk = (struct sock *)args->skaddr;
    u64 pid = bpf_get_current_pid_tgid();
    if (newsk == NULL) {
        return 0;
    }

    u8 ipver = 0;
    u64 family = newsk->__sk_common.skc_family;
    u16 lport = 0, dport = 0;
    u32 net_ns_inum = 0;
    dport = newsk->__sk_common.skc_dport;
    lport = newsk->__sk_common.skc_num;

    net_ns_inum = newsk->__sk_common.skc_net.net->ns.inum;

    if (family == AF_INET) {
        struct ipv4_data_t data4 = {};
        data4.ts_us = bpf_ktime_get_ns();
        data4.pid = pid >> 32;
        ipver = 4;
        data4.ip = ipver;
        data4.net_ns = net_ns_inum;

        data4.saddr = newsk->__sk_common.skc_rcv_saddr;
        data4.daddr = newsk->__sk_common.skc_daddr;
        data4.state = newsk->__sk_common.skc_state;

        bpf_get_current_comm(&data4.task, sizeof(data4.task));
        // ipv4_events.perf_submit(ctx, &data4, sizeof(data4));
        ipv4_events.perf_submit(args, &data4, sizeof(data4));
    } else /* AF_INET6 */ {
        struct ipv6_data_t data6 = {};
        data6.ts_us = bpf_ktime_get_ns();
        data6.pid = pid >> 32;
        ipver = 6;
        data6.ip = ipver;
        data6.net_ns = net_ns_inum;
        
        bpf_probe_read_kernel(&data6.saddr, sizeof(data6.saddr), newsk->__sk_common.skc_v6_rcv_saddr.in6_u.u6_addr32);
        bpf_probe_read_kernel(&data6.daddr, sizeof(data6.daddr), newsk->__sk_common.skc_v6_daddr.in6_u.u6_addr32);
        data6.state = newsk->__sk_common.skc_state;

        bpf_get_current_comm(&data6.task, sizeof(data6.task));
        // ipv6_events.perf_submit(ctx, &data6, sizeof(data6));
        ipv6_events.perf_submit(args, &data6, sizeof(data6));
    }
    return 0;
}
