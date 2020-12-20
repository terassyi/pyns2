from bcc import BPF
from bcc.utils import printb
from socket import inet_ntop, AF_INET, AF_INET6
from struct import pack

b = None




def print_ipv6_event(cpu, data, size):
    event = b["ipv6_events"].event(data)
    printb(b"%-7d %-12.12s %-2d %-16s %-5d %-16s %-5d %-12s %7d" % (event.pid,
        event.task, 
        event.ip,
        inet_ntop(AF_INET6, event.daddr).encode(),
        event.dport,
        inet_ntop(AF_INET6, event.saddr).encode(),
        event.lport,
        tcpstate2str(event.state),
        event.net_ns))

def tcpstate2str(state):
    # from include/net/tcp_states.h:
    tcpstate = {
        1: b"ESTABLISHED",
        2: b"SYN_SENT",
        3: b"SYN_RECV",
        4: b"FIN_WAIT1",
        5: b"FIN_WAIT2",
        6: b"TIME_WAIT",
        7: b"CLOSE",
        8: b"CLOSE_WAIT",
        9: b"LAST_ACK",
        10: b"LISTEN",
        11: b"CLOSING",
        12: b"NEW_SYN_RECV",
    }

    if state in tcpstate:
        return tcpstate[state]
    else:
        return bytes(state)


def tcp_info():

    def print_ipv4_event(cpu, data, size):
        event = b["ipv4_events"].event(data)
        printb(b"%-7d %-12.12s %-2d %-16s %-5d %-16s %-5d %-12s %-7d " % (event.pid,
            event.task, event.ip,
            inet_ntop(AF_INET, pack("I", event.daddr)).encode(),
            event.dport,
            inet_ntop(AF_INET, pack("I", event.saddr)).encode(),
            event.lport,
            tcpstate2str(event.state), 
            event.net_ns))

    prog = ""
    with open("bpf_prog/tcp_info.c") as f:
        prog = f.read()
    b = BPF(text=prog)

    print(b)

    b["ipv4_events"].open_perf_buffer(print_ipv4_event, page_cnt=64)
    b["ipv6_events"].open_perf_buffer(print_ipv6_event, page_cnt=64)

    print(b["ipv4_events"])
    while 1:
        try:
            b.perf_buffer_poll()
        except KeyboardInterrupt:
            exit()

if __name__ == '__main__':
    tcp_info()
