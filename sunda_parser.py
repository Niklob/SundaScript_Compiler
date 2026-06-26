class NodeAST:
    def citak_tangkal(self, undak=0):
        raise NotImplementedError

class NodeDeklarasi(NodeAST):
    def __init__(self, identifier, ajen_node):
        self.identifier = identifier
        self.ajen_node = ajen_node

    def citak_tangkal(self, undak=0):
        indent = "    " * undak
        print(f"{indent}└── [Node: DeklarasiVariabel]")
        print(f"{indent}    ├── ID  : {self.identifier}")
        self.ajen_node.citak_tangkal(undak + 1)

class NodeTembongkeun(NodeAST):
    def __init__(self, ajen_node):
        self.ajen_node = ajen_node

    def citak_tangkal(self, undak=0):
        indent = "    " * undak
        print(f"{indent}└── [Node: PerintahCitak (tembongkeun)]")
        self.ajen_node.citak_tangkal(undak + 1)

class NodeTanyakeun(NodeAST):
    def citak_tangkal(self, undak=0):
        indent = "    " * undak
        print(f"{indent}└── [Node: FungsiInput (tanyakeun)]")

class NodeKondisional(NodeAST):
    def __init__(self, simpul_kenca, operator, simpul_katuhu, blok_upami, blok_salian=None):
        self.simpul_kenca = simpul_kenca
        self.operator = operator
        self.simpul_katuhu = simpul_katuhu
        self.blok_upami = blok_upami
        self.blok_salian = blok_salian

    def citak_tangkal(self, undak=0):
        indent = "    " * undak
        print(f"{indent}└── [Node: Kondisional (sugan_wae)]")
        syarat_kenca = self.simpul_kenca.ngaran if isinstance(self.simpul_kenca, NodeVariabel) else self.simpul_kenca.ajen
        syarat_katuhu = self.simpul_katuhu.ngaran if isinstance(self.simpul_katuhu, NodeVariabel) else self.simpul_katuhu.ajen
        print(f"{indent}    ├── Syarat: {syarat_kenca} {self.operator} {syarat_katuhu}")
        print(f"{indent}    ├── Blok TRUE:")
        for n in self.blok_upami:
            n.citak_tangkal(undak + 2)
        if self.blok_salian:
            print(f"{indent}    └── Blok FALSE (lamun_henteu):")
            for n in self.blok_salian:
                n.citak_tangkal(undak + 2)

class NodeLiteral(NodeAST):
    def __init__(self, tipe, ajen):
        self.tipe = tipe
        self.ajen = ajen

    def citak_tangkal(self, undak=0):
        indent = "    " * undak
        print(f"{indent}└── [{self.tipe}] -> Ajen: {self.ajen}")

class NodeOperasiAritmatika(NodeAST):
    def __init__(self, operator, simpul_kenca, simpul_katuhu):
        self.operator = operator
        self.simpul_kenca = simpul_kenca
        self.simpul_katuhu = simpul_katuhu

    def citak_tangkal(self, undak=0):
        indent = "    " * undak
        print(f"{indent}└── [Node: Aritmatika ({self.operator})]")
        self.simpul_kenca.citak_tangkal(undak + 1)
        self.simpul_katuhu.citak_tangkal(undak + 1)

class NodeVariabel(NodeAST):
    def __init__(self, ngaran):
        self.ngaran = ngaran

    def citak_tangkal(self, undak=0):
        indent = "    " * undak
        print(f"{indent}└── [Variabel] -> Ngaran: {self.ngaran}")


class ParserSunda:
    def __init__(self, daptar_token):
        self.token_token = daptar_token
        self.posisi = 0

    def token_ayeuna(self):
        if self.posisi < len(self.token_token):
            return self.token_token[self.posisi]
        return None

    def maju(self):
        self.posisi += 1

    def cocogkeun(self, rupa_diharepkeun, ajen_diharepkeun=None):
        t = self.token_ayeuna()
        if t and t[0] == rupa_diharepkeun:
            if ajen_diharepkeun is None or t[1] == ajen_diharepkeun:
                self.maju()
                return t
        token_salah = t[1] if t else "POKOK PROGRAM SEEP"
        raise SyntaxError(f"[SYNTAX ERROR]: Urutan kode anjeun lepat dina kecap '{token_salah}'")

    def parse(self):
        daptar_instruksi = []
        while self.token_ayeuna() is not None:
            if self.token_ayeuna()[0] == 'SEPARATOR':
                self.maju()
                continue
            daptar_instruksi.append(self.parse_instruksi())
        return daptar_instruksi

    def parse_instruksi(self):
        t = self.token_ayeuna()
        if t[0] == 'KEYWORD' and t[1] == 'jieun':
            return self.parse_deklarasi()
        elif t[0] == 'KEYWORD' and t[1] == 'tembongkeun':
            return self.parse_tembongkeun()
        elif t[0] == 'KEYWORD' and t[1] == 'sugan_wae':
            return self.parse_sugan_wae()
        else:
            raise SyntaxError(f"[SYNTAX ERROR]: Teu terang kedah kumaha kana '{t[1]}'")

    def parse_deklarasi(self):
        self.cocogkeun('KEYWORD', 'jieun')
        var_token = self.cocogkeun('IDENTIFIER')
        
        # PERUBAHAN DI SINI: Cukup periksa kategori ASSIGN tanpa mengunci teks 'eta'
        self.cocogkeun('ASSIGN')
        
        t1 = self.token_ayeuna()
        if t1 and t1[0] == 'KEYWORD' and t1[1] == 'tanyakeun':
            self.maju()
            return NodeDeklarasi(var_token[1], NodeTanyakeun())
            
        elif t1 and t1[0] in ('NUMBER', 'STRING', 'IDENTIFIER'):
            self.maju()
            t2 = self.token_ayeuna()
            if t2 and t2[0] == 'OPERATOR':
                op = t2[1]
                self.maju()
                t3 = self.token_ayeuna()
                if t3 and t3[0] in ('NUMBER', 'STRING', 'IDENTIFIER'):
                    self.maju()
                    node_kenca = NodeVariabel(t1[1]) if t1[0] == 'IDENTIFIER' else NodeLiteral(t1[0], t1[1])
                    node_katuhu = NodeVariabel(t3[1]) if t3[0] == 'IDENTIFIER' else NodeLiteral(t3[0], t3[1])
                    return NodeDeklarasi(var_token[1], NodeOperasiAritmatika(op, node_kenca, node_katuhu))
                else:
                    raise SyntaxError("[SYNTAX ERROR]: Saatos operator kedah aya ajen anu sah!")
            else:
                node_ajen = NodeVariabel(t1[1]) if t1[0] == 'IDENTIFIER' else NodeLiteral(t1[0], t1[1])
                return NodeDeklarasi(var_token[1], node_ajen)
        else:
            raise SyntaxError("[SYNTAX ERROR]: Saatos kecap 'eta'/'itu' kedah aya ajen anu sah atanapi kecap 'tanyakeun'!")

    def parse_tembongkeun(self):
        self.cocogkeun('KEYWORD', 'tembongkeun')
        target_token = self.token_ayeuna()
        if target_token and target_token[0] in ('NUMBER', 'STRING', 'IDENTIFIER'):
            self.maju()
            node_target = NodeVariabel(target_token[1]) if target_token[0] == 'IDENTIFIER' else NodeLiteral(target_token[0], target_token[1])
            return NodeTembongkeun(node_target)
        else:
            raise SyntaxError("[SYNTAX ERROR]: Parentah 'tembongkeun' peryogi hal anu kedah dicitak!")

    def parse_sugan_wae(self):
        self.cocogkeun('KEYWORD', 'sugan_wae')
        
        t1 = self.token_ayeuna()
        self.maju()
        
        op = self.cocogkeun('OPERATOR')[1]
        
        t2 = self.token_ayeuna()
        self.maju()
        
        node_kenca = NodeVariabel(t1[1]) if t1[0] == 'IDENTIFIER' else NodeLiteral(t1[0], t1[1])
        node_katuhu = NodeVariabel(t2[1]) if t2[0] == 'IDENTIFIER' else NodeLiteral(t2[0], t2[1])
        
        self.cocogkeun('SEPARATOR')
        blok_upami = []
        while self.token_ayeuna() and not (self.token_ayeuna()[0] == 'KEYWORD' and self.token_ayeuna()[1] in ('lamun_henteu', 'tungtungna')):
            if self.token_ayeuna()[0] == 'SEPARATOR':
                self.maju()
                continue
            blok_upami.append(self.parse_instruksi())
            
        blok_salian = None
        if self.token_ayeuna() and self.token_ayeuna()[1] == 'lamun_henteu':
            self.maju()
            self.cocogkeun('SEPARATOR')
            blok_salian = []
            while self.token_ayeuna() and not (self.token_ayeuna()[0] == 'KEYWORD' and self.token_ayeuna()[1] == 'tungtungna'):
                if self.token_ayeuna()[0] == 'SEPARATOR':
                    self.maju()
                    continue
                blok_salian.append(self.parse_instruksi())
                
        self.cocogkeun('KEYWORD', 'tungtungna')
        return NodeKondisional(node_kenca, op, node_katuhu, blok_upami, blok_salian)