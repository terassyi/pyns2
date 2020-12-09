#include <uapi/linux/ptrace.h>
#include <net/sock.h>
#include <bcc/proto.h>
#include <linux/bpf.h>

#define IP_TCP 6
#define IP_UDP 17
#define IP_ICMP 1
#define ETH_HLEN 14

BPF_PERF_OUTPUT(skb_events);
BPF_HASH(packet_cnt, u64, long, 256); 

int packet_monitor(struct __sk_buff *skb) {

    u8 *cursor = 0;
    u32 saddr, daddr;
    long* count = 0;
    long one = 1;
    u64 pass_value = 0;
    
    struct ethernet_t *ethernet = cursor_advance(cursor, sizeof(*ethernet));
    struct ip_t *ip = cursor_advance(cursor, sizeof(*ip));
    if (ip->nextp != IP_TCP) 
    {
        if (ip -> nextp != IP_UDP) 
        {
            if (ip -> nextp != IP_ICMP) 
                return 0; 
        }
    }
    
    saddr = ip -> src;
    daddr = ip -> dst;
    pass_value = saddr;
    pass_value = pass_value << 32;
    pass_value = pass_value + daddr;
    count = packet_cnt.lookup(&pass_value); 
    if (count)  // check if this map exists
        *count += 1;
    else        // if the map for the key doesn't exist, create one
        {
            packet_cnt.update(&pass_value, &one);
        }
    return -1;
}
