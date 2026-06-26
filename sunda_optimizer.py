from sunda_parser import NodeDeklarasi, NodeTembongkeun, NodeOperasiAritmatika, NodeLiteral, NodeVariabel, NodeTanyakeun, NodeKondisional

class OptimizerSunda:
    def __init__(self):
        self.variabel_terpake = set()

    def optimasi(self, list_node_ast):
        print("=== PROSES OPTIMASI KODE DIMITIAN ===")
        for node in list_node_ast:
            self.parios_pamakéan(node)
            
        ast_teroptimasi = []
        for node in list_node_ast:
            if isinstance(node, NodeDeklarasi) and node.identifier not in self.variabel_terpake:
                print(f"[DEAD CODE ELIMINATION]: Ngahapus baris variabel mubazir '{node.identifier}'")
                continue
            
            node_baru = self.lipat_konstanta(node)
            ast_teroptimasi.append(node_baru)
            
        return ast_teroptimasi

    # LERESKEN: Nami fungsi parantos loyog sareng anu dicalukan janten parios_pamakéan
    def parios_pamakéan(self, node):
        if isinstance(node, NodeTembongkeun):
            if isinstance(node.ajen_node, NodeVariabel):
                self.variabel_terpake.add(node.ajen_node.ngaran)
        elif isinstance(node, NodeDeklarasi):
            self.parios_pamakéan_node(node.ajen_node)
        elif isinstance(node, NodeKondisional):
            self.parios_pamakéan_node(node.simpul_kenca)
            self.parios_pamakéan_node(node.simpul_katuhu)
            for sn in node.blok_upami: 
                self.parios_pamakéan(sn)
            if node.blok_salian:
                for sn in node.blok_salian: 
                    self.parios_pamakéan(sn)

    def parios_pamakéan_node(self, node):
        if isinstance(node, NodeVariabel):
            self.variabel_terpake.add(node.ngaran)
        elif isinstance(node, NodeOperasiAritmatika):
            self.parios_pamakéan_node(node.simpul_kenca)
            self.parios_pamakéan_node(node.simpul_katuhu)

    def lipat_konstanta(self, node):
        if isinstance(node, (NodeTanyakeun, NodeKondisional)):
            if isinstance(node, NodeKondisional):
                node.blok_upami = [self.lipat_konstanta(sn) for sn in node.blok_upami]
                if node.blok_salian:
                    node.blok_salian = [self.lipat_konstanta(sn) for sn in node.blok_salian]
            return node
            
        if isinstance(node, NodeDeklarasi):
            node.ajen_node = self.lipat_konstanta(node.ajen_node)
            return node
            
        elif isinstance(node, NodeOperasiAritmatika):
            kenca = self.lipat_konstanta(node.simpul_kenca)
            katuhu = self.lipat_konstanta(node.simpul_katuhu)
            
            if isinstance(kenca, NodeLiteral) and kenca.tipe == 'NUMBER' and \
               isinstance(katuhu, NodeLiteral) and katuhu.tipe == 'NUMBER':
                hasil = 0
                if node.operator == '+': hasil = kenca.ajen + katuhu.ajen
                elif node.operator == '-': hasil = kenca.ajen - katuhu.ajen
                elif node.operator == '*': hasil = kenca.ajen * katuhu.ajen
                elif node.operator == '/': hasil = kenca.ajen // katuhu.ajen
                
                print(f"[CONSTANT FOLDING]: Nyederhanakeun operasi {kenca.ajen} {node.operator} {katuhu.ajen} -> {hasil}")
                return NodeLiteral('NUMBER', hasil)
            
            node.simpul_kenca = kenca
            node.simpul_katuhu = katuhu
            return node
            
        elif isinstance(node, NodeTembongkeun):
            node.ajen_node = self.lipat_konstanta(node.ajen_node)
            return node
            
        return node