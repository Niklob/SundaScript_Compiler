import sys
import re
from lexer import LexerSunda
from sunda_parser import ParserSunda
from sunda_semantic import AnalisisSemantikSunda
from sunda_optimizer import OptimizerSunda
from sunda_codegen import SundaCodeGenerator

class DualOutput:
    """Kelas untuk menduplikasi output terminal langsung ke dalam file txt tertentu"""
    def __init__(self, nama_file):
        self.terminal = sys.stdout
        # Menggunakan mode 'w' agar setiap running menghasilkan file yang bersih/terbaru
        self.log_file = open(nama_file, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log_file.write(message)

    def flush(self):
        self.terminal.flush()
        self.log_file.flush()

    def close(self):
        self.log_file.close()

def tentukan_nama_file(kode_asal):
    """Menentukan nama file txt secara terpisah berdasarkan konteks prompt"""
    if "ngaran_mhs" in kode_asal:
        return "hasil_ngaran_mhs.txt"
    elif "x" in kode_asal or "10" in kode_asal:
        return "hasil_operasi_x.txt"
    else:
        return "hasil_kompilasi_lainnya.txt"

def jalankeun_kompiler(kode_asal):
    """Fungsi pikeun mrosés blok kode sarta nunda hasilna ka file txt anu kapisah"""
    if not kode_asal.strip():
        return
        
    # Menentukan nama file secara otomatis dan dinamis
    nama_file_target = tentukan_nama_file(kode_asal)
    
    stdout_asli = sys.stdout
    dual_output = DualOutput(nama_file_target)
    sys.stdout = dual_output
    
    try:
        print("="*50)
        print("        MIMITIAN PROSES KOMPILASI AYEUNA PISAN")
        print(f"        PROMPT INPUT: {kode_asal.replace('\n', '; ')}")
        print("="*50)
        
        # 1. Tahap Nyieun Token (Lexer)
        lexer = LexerSunda(kode_asal)
        tokens = lexer.candak_sadaya_token()
        print("\n[FASE 1] HASIL ANALISIS LEXER (7 KATEGORI TOKEN):")
        for t in tokens:
            print(f"  Token Kategori: {t[0]:<12} | Ajen Téks: {t[1]}")
        
        # 2. Tahap Analisis Struktur (Parser & AST)
        parser = ParserSunda(tokens)
        try:
            ast = parser.parse()
        except SyntaxError as e:
            print(e)
            return

        print("\n[FASE 2] VISUALISASI AST SATEUACAN OPTIMASI:")
        for node in ast:
            node.citak_tangkal()
            
        # 3. Tahap Validasi Aturan & Hartos Data (Analisis Semantik)
        print("\n[FASE 3] PROSES ANALISIS SEMANTIK:")
        semantic = AnalisisSemantikSunda()
        try:
            semantic.analisis(ast)
        except Exception as e:
            print(e)
            return

        # 4. Tahap Saderhanakeun Struktur Kode (Optimizer)
        print("\n[FASE 4] PROSES OPTIMASI KODE AST:")
        optimizer = OptimizerSunda()
        ast_teroptimasi = optimizer.optimasi(ast)
        
        print("\nVISUALISASI AST SAATOS OPTIMASI (SIAP GENERATE):")
        for node in ast_teroptimasi:
            node.citak_tangkal()

        # 5. Tahap Konversi Akhir ka Kode Assembly (Code Generator)
        print("\n[FASE 5] PROSES GENERASI KODE TARGET:")
        generator = SundaCodeGenerator()
        kode_target = generator.generate(ast_teroptimasi)
        
        print("\nHASIL GENERATOR KODE AKHIR (TARGET ASSEMBLY):")
        print("=" * 50)
        print(kode_target)
        print("=" * 50)
        
    finally:
        # Mengembalikan sistem output ke kondisi normal setelah selesai
        sys.stdout = stdout_asli
        dual_output.close()
        print(f"\n[INFO]: Log kompilasi sukses dipisahkeun ka file: '{nama_file_target}'")

def main():
    print("==================================================")
    print("   WILUJEUNG SUMPING DINA SUNDASCRIPT INTERACTIVE COMPILER")
    print("   Hasil eksekusi otomatis dipisah dumasar kana prompt!")
    print("   Serat 'kaluar' pikeun ngeureunkeun program.")
    print("==================================================")
    
    while True:
        try:
            print("\nSundaScript> ", end="")
            input_pangguna = input()
            
            if input_pangguna.strip().lower() == 'kaluar':
                print("\nParantos réséh, Kang/Téh! Hatur nuhun tos nyobian SundaScript.")
                break
                
            kode_beresih = input_pangguna.replace(";", "\n")
            jalankeun_kompiler(kode_beresih)
            
        except (KeyboardInterrupt, EOFError):
            print("\n\nParantos réséh, Kang/Téh! Hatur nuhun tos nyobian SundaScript.")
            break

if __name__ == "__main__":
    main()

