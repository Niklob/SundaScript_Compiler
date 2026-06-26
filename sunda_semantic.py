from sunda_parser import NodeDeklarasi, NodeTembongkeun, NodeOperasiAritmatika, NodeLiteral, NodeVariabel, NodeTanyakeun, NodeKondisional

class AnalisisSemantikSunda:
    def __init__(self):
        self.tabel_simbol = {}

    def analisis(self, daptar_node_ast):
        
        print("=== MIMITIAN ANALISIS SEMANTIK ===")
        for node in daptar_node_ast:
            self.longok(node)
        print("[STATUS SEMANTIK]: Aman Kang/Téh, hartos & rupa data parantos sah!")

    def longok(self, node):
        nami_metode = f"longok_{type(node).__name__}"
        metode = getattr(self, nami_metode, self.longok_default)
        return metode(node)

    def longok_default(self, node):
        raise Exception(f"Metode longok_{type(node).__name__} acan dijieun.")

    def longok_NodeDeklarasi(self, node):
        var_nami = node.identifier
        if var_nami in self.tabel_simbol:
            raise TypeError(f"[SEMANTIC ERROR]: Variabel '{var_nami}' parantos dijieun sateuacanna, Kang!")
        
        tipe_ajen = self.longok(node.ajen_node)
        self.tabel_simbol[var_nami] = tipe_ajen
        print(f"[TABEL SIMBOL DIPANJANGKEUN]: {var_nami} -> Tipe: {tipe_ajen}")

    def longok_NodeOperasiAritmatika(self, node):
        tipe_kenca = self.longok(node.simpul_kenca)
        tipe_katuhu = self.longok(node.simpul_katuhu)
        if tipe_kenca != 'NUMBER' or tipe_katuhu != 'NUMBER':
            raise TypeError(f"[SEMANTIC ERROR]: Logika ngaco dina aritmatika!")
        return 'NUMBER'

    def longok_NodeTembongkeun(self, node):
        self.longok(node.ajen_node)

    def longok_NodeLiteral(self, node):
        return node.tipe

    def longok_NodeVariabel(self, node):
        var_nami = node.ngaran
        if var_nami not in self.tabel_simbol:
            raise NameError(f"[SEMANTIC ERROR]: Anjeun hoyong nyambat '{var_nami}', tapi variabelna acan dijieun!")
        return self.tabel_simbol[var_nami]

    def longok_NodeTanyakeun(self, node):
        return 'STRING'

    # REVISI: Analisis Semantik pikeun Validasi Cabang Kondisional
    def longok_NodeKondisional(self, node):
        self.longok(node.simpul_kenca)
        self.longok(node.simpul_katuhu)
        for sub_node in node.blok_upami:
            self.longok(sub_node)
        if node.blok_salian:
            for sub_node in node.blok_salian:
                self.longok(sub_node)
        return None