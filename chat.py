import socket, sys, threading, os
import des1 as des

mode = sys.argv[1]                       
key = des.make_key(sys.argv[2])         
host = sys.argv[3] if len(sys.argv) > 3 else "127.0.0.1"
PORT = 5000

if mode == "listen":
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", PORT))
    server.listen(1)
    print("Menunggu...")
    sock, _ = server.accept()
    nama = "Receiver"
else:
    sock = socket.create_connection((host, PORT))
    nama = "Sender"
print("Terhubung")

def terima():
    try:
        for baris in sock.makefile("r"):       
            cipher = baris.strip()
            print("\nCiphertext:", cipher)
            try:
                print("Plaintext :", des.decrypt(cipher, key))
            except Exception:
                print("Gagal dekripsi")
    except OSError:
        pass       
    print("\nProgram berhenti")
    os._exit(0)

threading.Thread(target=terima, daemon=True).start()

try:
    while True:
        teks = input()
        if teks == "exit":
            break
        cipher = des.encrypt(f"{nama}: {teks}", key)
        print("Plaintext :", teks)
        print("Ciphertext:", cipher)
        sock.sendall((cipher + "\n").encode())  
except (KeyboardInterrupt, EOFError):
    pass
except OSError:
    print("Gagal mengirim koneksi terputus.")
finally:
    try:
        sock.shutdown(socket.SHUT_RDWR)    
    except OSError:
        pass
    sock.close()
    os._exit(0)