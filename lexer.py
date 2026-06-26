import re

class LexerSunda:
    def __init__(self, kode_asal):
        self.kode = kode_asal
        self.token_token = []
        # Keyword dinamis saluyu sareng paréntah dosén (kaasup 'sugan_wae' sarta 'lamun_henteu')
        self.keyword_sunda = {'jieun', 'sugan_wae', 'lamun_henteu', 'tungtungna', 'nguriling', 'tembongkeun', 'tanyakeun'}

    def candak_sadaya_token(self):
        pola_token = [
            ('STRING',     r'"[^"\n]*"'),                     
            ('NUMBER',     r'\d+'),                           
            ('OPERATOR',   r'==|<=|>=|[\+\-\*/<>]'),          
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),        
            ('SEPARATOR',  r'\n'),                            
            ('MISC',       r'[ \t\r]+'),                      
        ]
        
        regex_induk = '|'.join(f'(?P<{nami}>{pola})' for nami, pola in pola_token)
        
        for panyocog in re.finditer(regex_induk, self.kode):
            rupa_token = panyocog.lastgroup
            ajen_token = panyocog.group(rupa_token)
            
            if rupa_token == 'MISC':
                continue
                
            elif rupa_token == 'IDENTIFIER':
                if ajen_token in self.keyword_sunda:
                    self.token_token.append(('KEYWORD', ajen_token)) 
                # PERUBAHAN DI SINI: Mendukung kata 'eta' maupun 'itu' sebagai ASSIGN
                elif ajen_token in ('eta', 'itu'):
                    self.token_token.append(('ASSIGN', ajen_token))   
                else:
                    self.token_token.append(('IDENTIFIER', ajen_token)) 
                    
            elif rupa_token == 'NUMBER':
                self.token_token.append(('NUMBER', int(ajen_token)))  
                
            elif rupa_token == 'STRING':
                self.token_token.append(('STRING', ajen_token[1:-1])) 
                
            elif rupa_token == 'OPERATOR':
                self.token_token.append(('OPERATOR', ajen_token))     
                
            elif rupa_token == 'SEPARATOR':
                self.token_token.append(('SEPARATOR', '\\n'))          
        return self.token_token