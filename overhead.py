import subprocess, csv, os
files = [
    'Task1_PDR_21.pcapng','Task1_PDR_22.pcapng','Task1_PDR_23.pcapng',
    'Task1_PDR_24.pcapng','Task1_PDR_25.pcapng','Task1_PDR_26.pcapng',
    'Task1_PDR_27.pcapng','Task1_PDR_28.pcapng','Task1_PDR_29.pcapng',
    'Task1_PDR_30.pcapng','Task1_PDR_31.pcapng','Task1_PDR_32.pcapng',
    'Task1_PDR_33.pcapng','Task1_PDR_34.pcapng','Task1_PDR_35.pcapng','Task1_PDR_36.pcapng',
    'Task1_PDR_37.pcapng','Task1_PDR_38.pcapng','Task1_PDR_39.pcapng',
    'Task1_PDR_40.pcapng','Task1_PDR_41.pcapng','Task1_PDR_42.pcapng',
    'Task1_PDR_43.pcapng','Task1_PDR_44.pcapng'
]
def get_stats(f, filt=None):
    cmd = ['tshark', '-r', f, '-q', '-z', 'io,stat,0']
    if filt:
        cmd += ['-2', '-R', filt]
    out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode()
    for line in out.splitlines():
        if '<>' in line:
            parts = [x.strip() for x in line.split('|') if x.strip()]
            if len(parts) >= 3:
                return parts[1], parts[2]
    return '0', '0'
print("Verifying filter on Task1_PDR_45.pcapng...")   
tf, tb = get_stats('Task1_PDR_45.pcapng')
cf, cb = get_stats('Task1_PDR_45.pcapng', 'coap')
mf, mb = get_stats('Task1_PDR_45.pcapng', 'mle')
print(f"  Total:  {tf} frames")
print(f"  CoAP:   {cf} frames")
print(f"  MLE:    {mf} frames")
if cf == tf:
    print("WARNING: filter still not working, check tshark version")
else:
    print("Filter working, running all files...")
    with open('overhead.csv', 'w', newline='') as csvfile:
        w = csv.writer(csvfile)
        w.writerow(['filename','total_frames','total_bytes','coap_frames','coap_bytes',
                    'mle_frames','mle_bytes','overhead_frames','overhead_pct'])
        for f in files:
            if not os.path.exists(f):
                print(f'MISSING: {f}')
                continue
            tf, tb = get_stats(f)
            cf, cb = get_stats(f, 'coap')
            mf, mb = get_stats(f, 'mle')
            overhead = int(tf) - int(cf)
            pct = round(overhead / int(tf) * 100, 2) if int(tf) > 0 else 0
            w.writerow([f, tf, tb, cf, cb, mf, mb, overhead, pct])
            print(f'Done: {f} | total={tf} coap={cf} mle={mf} overhead={pct}%')

    print('Saved to overhead.csv')