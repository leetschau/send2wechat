import i3ipc
import subprocess
import glob


def get_sock() -> str:
    # i3 socket path is a string like '/run/user/1000/i3/ipc-socket.3614'
    current_sock = subprocess.check_output(
            ['i3', '--get-socketpath']).decode('utf-8').strip()
    sock_ptn = current_sock.split('.')[0] + '.*'
    assert(len(current_sock.split('.')) == 2)
    all_socks = glob.glob(sock_ptn)
    # we can only determine the target socket when there are 2 sockets:
    # one is the current socket, the other is the target socket
    assert(len(all_socks) == 2)
    target_sock = set(all_socks) - set([current_sock])
    assert(len(target_sock) == 1)
    return target_sock.pop()


tmpFile = '/tmp/xdotoolscripts'

i3wechat = i3ipc.Connection(get_sock())
raw = subprocess.check_output(["xsel", "-bo"]).decode('utf-8')
# msg = raw.replace("'", "`")
with open(tmpFile, 'w') as f:
    f.write(raw)
i3wechat.command(f'exec xdotool type --file {tmpFile}')
