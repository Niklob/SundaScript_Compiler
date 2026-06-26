from sunda_parser import NodeDeklarasi, NodeTembongkeun, NodeOperasiAritmatika, NodeLiteral, NodeVariabel, NodeTanyakeun, NodeKondisional

class SundaCodeGenerator:
    def __init__(self):
        self.indeks_register = 0
        self.indeks_label = 0
        self.kode_target = []

    def jieun_register_anyar(self):
        self.indeks_register += 1
        return f"R{self.indeks_register}"

    def jieun_label_anyar(self):
        self.indeks_label += 1
        return f"LABEL_{self.indeks_label}"

    def generate(self, daptar_node_ast):
        print("=== PROSES GENERASI KODE TARGET (ASSEMBLY-LIKE) ===")
        self.kode_target.append("; --- MIMITI KODE KOMPILASI SUNDASCRIPT ---")
        for node in daptar_node_ast:
            self.longok(node)
        self.kode_target.append("; --- TUNGTUNG PROGRAM HALT ---")
        return "\n".join(self.kode_target)

    def longok(self, node):
        if isinstance(node, NodeDeklarasi):
            reg_data = self.longok_node(node.ajen_node)
            self.kode_target.append(f"STORE  {node.identifier}, {reg_data}")
            
        elif isinstance(node, NodeTembongkeun):
            reg_output = self.longok_node(node.ajen_node)
            self.kode_target.append(f"PRINT  {reg_output}")
            
        elif isinstance(node, NodeKondisional):
            reg_kenca = self.longok_node(node.simpul_kenca)
            reg_katuhu = self.longok_node(node.simpul_katuhu)
            label_false = self.jieun_label_anyar()
            label_end = self.jieun_label_anyar()
            
            self.kode_target.append(f"CMP    {reg_kenca}, {reg_katuhu}")
            self.kode_target.append(f"JNE    {label_false}") 
            
            for sn in node.blok_upami: self.longok(sn)
            self.kode_target.append(f"JMP    {label_end}")
            
            self.kode_target.append(f"{label_false}:")
            if node.blok_salian:
                for sn in node.blok_salian: self.longok(sn)
                
            self.kode_target.append(f"{label_end}:")

    def longok_node(self, node):
        if isinstance(node, NodeLiteral):
            reg = self.jieun_register_anyar()
            val = f'"{node.ajen}"' if node.tipe == "STRING" else node.ajen
            self.kode_target.append(f"LOAD   {reg}, {val}")
            return reg
        elif isinstance(node, NodeVariabel):
            reg = self.jieun_register_anyar()
            self.kode_target.append(f"LOAD   {reg}, {node.ngaran}")
            return reg
        elif isinstance(node, NodeTanyakeun):
            reg = self.jieun_register_anyar()
            self.kode_target.append(f"SCAN   {reg}")
            return reg
        elif isinstance(node, NodeOperasiAritmatika):
            reg_kenca = self.longok_node(node.simpul_kenca)
            reg_katuhu = self.longok_node(node.simpul_katuhu)
            reg_hasil = self.jieun_register_anyar()
            op_code = "ADD" if node.operator == '+' else "SUB" if node.operator == '-' else "MUL" if node.operator == '*' else "DIV"
            self.kode_target.append(f"{op_code}    {reg_hasil}, {reg_kenca}, {reg_katuhu}")
            return reg_hasil