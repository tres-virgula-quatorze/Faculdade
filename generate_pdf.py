import os
from fpdf import FPDF
import urllib.request

# Download logo
try:
    urllib.request.urlretrieve('https://unigrande.edu.br/_next/static/media/logo-unigrande-color-blue.0251e5cb.png', 'logo.png')
except:
    pass

class PDF(FPDF):
    def cover(self):
        self.add_page()
        # Top banner
        self.set_fill_color(0, 51, 160)
        self.rect(0, 0, 210, 40, 'F')
        
        # Bottom accent
        self.set_fill_color(255, 102, 0)
        self.rect(0, 287, 210, 10, 'F')
        
        if os.path.exists('logo.png'):
            self.image('logo.png', x=75, y=10, w=60)
        
        self.ln(60)
        self.set_font('helvetica', 'B', 18)
        self.cell(0, 10, 'ANTONIO ERICK CONCEIÇÃO DA SILVA', new_x="LMARGIN", new_y="NEXT", align='C')
        
        self.ln(60)
        self.set_fill_color(230, 240, 255)
        self.set_font('helvetica', 'B', 28)
        self.set_text_color(0, 51, 160)
        self.cell(0, 30, '6 ARTICULAÇÕES SINOVIAIS', fill=True, new_x="LMARGIN", new_y="NEXT", align='C')
        self.set_text_color(0, 0, 0)
        
        self.set_y(250)
        self.set_font('helvetica', 'B', 14)
        self.cell(0, 10, 'Buriticupu - MA', new_x="LMARGIN", new_y="NEXT", align='C')
        self.cell(0, 10, '2026', new_x="LMARGIN", new_y="NEXT", align='C')

    def inside_cover(self):
        self.add_page()
        self.set_fill_color(0, 51, 160)
        self.rect(0, 0, 210, 5, 'F')
        
        self.set_y(40)
        self.set_font('helvetica', 'B', 18)
        self.cell(0, 10, 'ANTONIO ERICK CONCEIÇÃO DA SILVA', new_x="LMARGIN", new_y="NEXT", align='C')
        
        self.ln(40)
        self.set_font('helvetica', 'B', 24)
        self.set_text_color(0, 51, 160)
        self.cell(0, 15, '6 ARTICULAÇÕES SINOVIAIS', new_x="LMARGIN", new_y="NEXT", align='C')
        self.set_text_color(0, 0, 0)
        
        self.ln(40)
        self.set_x(100)
        self.set_font('helvetica', '', 12)
        
        self.set_fill_color(255, 102, 0)
        self.rect(95, self.get_y(), 2, 35, 'F')
        
        self.multi_cell(90, 8, 'Trabalho acadêmico apresentado ao Centro Universitário UniGrande, como requisito parcial para avaliação.\n\nProfessora: Bianca Lira', align='J')
        
        self.set_y(250)
        self.set_font('helvetica', 'B', 14)
        self.cell(0, 10, 'Buriticupu - MA', new_x="LMARGIN", new_y="NEXT", align='C')
        self.cell(0, 10, '2026', new_x="LMARGIN", new_y="NEXT", align='C')

pdf = PDF()
pdf.cover()
pdf.inside_cover()

html_content = """
<h1 align="center" style="color: #0033a0;">6 ARTICULAÇÕES SINOVIAIS</h1>
<p>As articulações sinoviais são o tipo mais comum e mais móvel de articulação no corpo humano. Elas se caracterizam pela presença de uma cápsula articular que envolve uma cavidade sinovial cheia de líquido sinovial, o qual atua como lubrificante. As superfícies ósseas em contato são recobertas por cartilagem hialina (cartilagem articular), garantindo um movimento suave e sem atrito. A seguir, são descritas 6 importantes articulações sinoviais do corpo humano.</p>

<h2 style="color: #ff6600;">1. Articulação Glenoumeral (Ombro)</h2>
<b>Classificação:</b> Sinovial Esferóide.<br>
<b>Ossos Envolvidos:</b> Escápula (cavidade glenóide) e Úmero (cabeça do úmero).<br>
<b>Movimentos:</b> Flexão, extensão, abdução, adução, rotação medial, rotação lateral e circundução.<br>
<i>É uma articulação multiaxial, permitindo uma ampla gama de movimentos. Devido à sua grande mobilidade, é também uma das articulações mais instáveis do corpo, dependendo fortemente do manguito rotador e dos ligamentos associados para sua estabilização.</i>

<h2 style="color: #ff6600;">2. Articulação Coxofemoral (Quadril)</h2>
<b>Classificação:</b> Sinovial Esferóide.<br>
<b>Ossos Envolvidos:</b> Osso do quadril (acetábulo) e Fêmur (cabeça do fêmur).<br>
<b>Movimentos:</b> Flexão, extensão, abdução, adução, rotação medial, rotação lateral e circundução.<br>
<i>Semelhante à articulação do ombro por ser esferóide, mas projetada para sustentação de peso e estabilidade profunda. O acetábulo é profundo e engloba grande parte da cabeça femoral, o que reduz sua amplitude em relação ao ombro, mas fornece uma articulação incrivelmente forte.</i>

<h2 style="color: #ff6600;">3. Articulação do Cotovelo (Umeroulnar e Umerorradial)</h2>
<b>Classificação:</b> Sinovial Gínglimo (Dobradiça).<br>
<b>Ossos Envolvidos:</b> Úmero (tróclea e capítulo), Ulna (incisura troclear) e Rádio (cabeça do rádio).<br>
<b>Movimentos:</b> Flexão e extensão.<br>
<i>Trata-se de uma articulação complexa que funciona principalmente como uma dobradiça (gínglimo), restringindo o movimento em grande parte a um único plano. É estabilizada por fortes ligamentos colaterais (ulnar e radial).</i>

<h2 style="color: #ff6600;">4. Articulação Tibiofemoral (Joelho)</h2>
<b>Classificação:</b> Sinovial Gínglimo Modificado (ou Bicondilar).<br>
<b>Ossos Envolvidos:</b> Fêmur (côndilos femorais) e Tíbia (côndilos tibiais), além da Patela (articulação patelofemoral).<br>
<b>Movimentos:</b> Flexão, extensão e leve rotação medial/lateral (quando flexionado).<br>
<i>É a maior articulação do corpo humano e suporta grande parte do peso corporal. Devido à incongruência entre os ossos, apresenta os meniscos (estruturas fibrocartilaginosas) que melhoram o encaixe. Permite primariamente flexão e extensão, com uma leve rotação quando flexionada.</i>

<h2 style="color: #ff6600;">5. Articulação Radiocarpal (Punho)</h2>
<b>Classificação:</b> Sinovial Elipsóide (Condilar).<br>
<b>Ossos Envolvidos:</b> Rádio (extremidade distal) e ossos do Carpo (escafoide, semilunar e piramidal).<br>
<b>Movimentos:</b> Flexão, extensão, abdução (desvio radial), adução (desvio ulnar) e circundução.<br>
<i>Esta articulação conecta o antebraço à mão. Sendo condilar, permite movimento em dois planos principais. O disco articular a separa da ulna, que não participa diretamente dessa articulação.</i>

<h2 style="color: #ff6600;">6. Articulação Temporomandibular (ATM)</h2>
<b>Classificação:</b> Sinovial Gínglimo Modificado / Plana.<br>
<b>Ossos Envolvidos:</b> Osso Temporal (fossa mandibular e tubérculo articular) e Mandíbula (cabeça ou côndilo da mandíbula).<br>
<b>Movimentos:</b> Elevação, depressão (abertura e fechamento da boca), protrusão, retração e movimentos de lateralidade.<br>
<i>É uma das articulações mais utilizadas no corpo humano (mastigação, fala, deglutição). Possui um disco articular que divide a cavidade sinovial em duas partes, permitindo tanto um movimento de dobradiça quanto um movimento de deslizamento.</i>
"""

pdf.add_page()
pdf.set_fill_color(255, 102, 0)
pdf.rect(0, 0, 210, 3, 'F')
pdf.set_fill_color(0, 51, 160)
pdf.rect(0, 3, 210, 7, 'F')
pdf.set_y(15)

pdf.write_html(html_content)

out_path = os.path.join(os.getcwd(), 'Trabalho_Articulacoes_Sinoviais_Completo.pdf')
pdf.output(out_path)
print('PDF generated:', out_path)
