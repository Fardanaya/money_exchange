import json

class MesinPenukaranUang:
    def __init__(self):
        self.load_ketersediaan_pecahan()

    def load_ketersediaan_pecahan(self):
        try:
            with open("ketersediaan_pecahan.json", "r") as file:
                self.ketersediaan_pecahan = json.load(file)
                # Konversi nilai string ke integer
                self.ketersediaan_pecahan = {int(k): v for k, v in self.ketersediaan_pecahan.items()}
        except FileNotFoundError:
            self.ketersediaan_pecahan = {
                # kiri pecahan uang, kanan stok
                100000: 1,
                50000: 2,
                20000: 5,
                10000: 10,
                5000: 20,
                2000: 50,
                1000: 100
            }
            self.save_ketersediaan_pecahan()

    def save_ketersediaan_pecahan(self):
        with open("ketersediaan_pecahan.json", "w") as file:
            json.dump(self.ketersediaan_pecahan, file, indent=4)
            
    def tambah_stok_pecahan(self, pecahan, jumlah):
        self.ketersediaan_pecahan[pecahan] += jumlah
        self.save_ketersediaan_pecahan()

    def cetak_daftar_pecahan(self):
        print("Daftar pecahan uang yang tersedia:")
        for index, (pecahan, stok) in enumerate(self.ketersediaan_pecahan.items(), start=1):
            print(f"{index}. {pecahan}")
        
    def pilih_pecahan_uang(self):
        self.cetak_daftar_pecahan()
        index_pecahan = int(input("Pilih nomor pecahan uang yang ingin dimasukkan: "))
        if 1 <= index_pecahan <= len(self.ketersediaan_pecahan):
            pecahan_uang = list(self.ketersediaan_pecahan.keys())[index_pecahan - 1]
            return pecahan_uang
        else:
            print("Pilihan tidak valid.")
            return None
    
    def cetak_pecahan_tersedia(self, jumlah_uang):
        pecahan_tersedia = {}
        index = 1
        for (pecahan, stock) in self.ketersediaan_pecahan.items():
            if pecahan <= jumlah_uang and jumlah_uang // pecahan <= stock:
                pecahan_tersedia[index] = (pecahan, stock)
                print(f"{index}. {pecahan}")
                index += 1
        return pecahan_tersedia
        
if __name__ == "__main__":
    mesin = MesinPenukaranUang()
    print("Selamat datang di mesin penukaran uang.")
    loop = 1
    while loop != 0:
        pecahan_uang = mesin.pilih_pecahan_uang()
        jumlah_lembar = int(input("Masukkan jumlah yang ingin ditukarkan: "))

        print(pecahan_uang)
        print(jumlah_lembar)
        jumlah_uang = pecahan_uang * jumlah_lembar
        print(jumlah_uang)
        print("Daftar pecahan uang yang bisa ditukarkan:")
        pecahan_tersedia = mesin.cetak_pecahan_tersedia(jumlah_uang)

        if not pecahan_tersedia:
            print("Maaf, tidak ada pecahan yang bisa ditukarkan untuk jumlah uang yang dimasukkan.")
            loop = int(input("Apakah ingin melanjutkan? (1 = ya, 0 = tidak): "))
            continue

        tukar = int(input("Pilih nomor pecahan yang ingin ditukarkan: "))

        if tukar in pecahan_tersedia:
            pecahan, stock = pecahan_tersedia[tukar]
            if pecahan_tersedia == None:
                print("Maaf, tidak ada pecahan yang bisa ditukarkan untuk jumlah uang yang dimasukkan.")
                print("Penukaran dibatalkan.")
                continue
            
            else:    
                print(f"Anda akan menukar uang sejumlah {jumlah_uang} dengan:")
                print(f"{pecahan} ({jumlah_uang // pecahan} lembar)")
                konfirmasi = input("Konfirmasi penukaran (1 = ya, 0 = tidak): ")
                if konfirmasi == '1':
                    mesin.ketersediaan_pecahan[pecahan] -= jumlah_uang // pecahan
                    mesin.tambah_stok_pecahan(pecahan_uang, jumlah_lembar)
                    mesin.save_ketersediaan_pecahan()
                else:
                    print("Penukaran dibatalkan.")
        else:
            print("Nomor pecahan yang dipilih tidak valid.")

        loop = int(input("Apakah ingin melanjutkan? (1 = ya, 0 = tidak): "))