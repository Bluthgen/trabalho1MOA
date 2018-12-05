# -*- coding: utf-8 -*-

import math
import random
from matplotlib import pyplot as plt

tamGenes= 0
tamPopulacao= 0

class Vertice:
    def __init__(self, nome:int, coords:tuple):
        self.nome= nome
        self.x, self.y= coords
        self.tipo= ""

    @staticmethod
    def distance(v1, v2):
            return math.hypot(v2.x - v1.x, v2.y - v1.y)
        
    
    def __repr__(self):
        return f'{self.nome}'

class GrafoCartesiano:
    def __init__(self):
        self.vertices= []
        
    def add(self, v):
        if isinstance(v, Vertice):
            self.vertices.append(v)
            
    
   # @property
   # def vertices(self):
   #     return self._vertices        
    
   
    
class Individuo:
    def __init__(self, grafo):
        self.genes= []
        self.idade= 0
        #self.genes= [Vertice(0, (13.799940281434441 ,  44.703335320869506)), Vertice(1, (4.929969173873872 ,  38.57085858780106)), Vertice(2, (13.272217821147253 ,  14.380034596293035)), Vertice(3, (12.886353710138925 ,  14.516591138225692)), Vertice(4, (4.637545238897739 ,  29.0476235222785)), Vertice(5, (26.704681673223963 ,  35.54304838007247)), Vertice(6, (10.31369713595877 ,  37.18167173541928)), Vertice(7, (40.86283402907582 ,  31.63313651370869)), Vertice(8, (35.686213695624595 ,  7.532421945058254)), Vertice(9, (5.472325177881782 ,  25.33350450976665))]
        self.genes= grafo.vertices.copy()
        random.shuffle(self.genes)
        self._adaptacao= 0
    
    def calculaAdaptacao(self):
        self.adaptacao= 0
        peso= 0
        for i in range(tamGenes - 1):
            peso= peso + Vertice.distance(self.genes[i],self.genes[i+1])
        peso= peso+ Vertice.distance(self.genes[tamGenes-1], self.genes[0])
        self.adaptacao= 1/peso
        
    def copy(self):
        copia= Individuo(GrafoCartesiano())
        copia.genes= self.genes.copy()
        copia.idade= self.idade
        copia.adaptacao= self.adaptacao
        return copia
        
class Populacao:
    def __init__(self):
        self.individuos= []
        self.maisAdaptado= 0
        
    def inicializaPopulacao(self, grafo):
        for i in range(tamPopulacao):
            self.individuos.append(Individuo(grafo))
        
    def getMaisAdaptado(self):
        maxAdapt= -1
        maxAdaptIndice= 0
        for i in range(tamPopulacao):
            if maxAdapt <= self.individuos[i].adaptacao:
                maxAdapt= self.individuos[i].adaptacao
                maxAdaptIndice= i
        self.maisAdaptado= self.individuos[maxAdaptIndice].adaptacao
        return self.individuos[maxAdaptIndice]
    
    def getSegundoMaisAdaptado(self):
        maxAdapt1= 0
        maxAdapt2= 0
        for i in range(tamPopulacao):
            if self.individuos[i].adaptacao > self.individuos[maxAdapt1].adaptacao:
                maxAdapt2= maxAdapt1
                maxAdapt1= i
            elif self.individuos[i].adaptacao > self.individuos[maxAdapt2].adaptacao:
                maxAdapt2= i
        return self.individuos[maxAdapt2]
    
    def getMaisAdaptados(self):
        lista= []
        menores= self.getMenosAdaptados()
        maior= menores[0]
        for j in range(0, tamPopulacao/2):
            for i in range(0, tamPopulacao):
                if self.individuos[i].adaptacao > self.individuos[maior].adaptacao and not i in lista:
                    maior= i
            lista.append(maior)
            maior= menores[0]
        return lista
    
    def getDoisMenosAdaptados(self):
        minAdapt1= 0
        minAdapt2= 0
        for i in range(tamPopulacao):
            if self.individuos[minAdapt1].adaptacao >= self.individuos[i].adaptacao:
                minAdapt2= minAdapt1
                minAdapt1= i
            elif self.individuos[minAdapt2].adaptacao >= self.individuos[i].adaptacao:
                minAdapt2= i
        return (minAdapt1, minAdapt2)
    
    def getDoisMaisVelhos(self):
        maxIdade1= 0
        maxIdade2= 0
        for i in range(tamPopulacao):
            if self.individuos[i].idade > self.individuos[maxIdade1].idade:
                maxIdade2= maxIdade1
                maxIdade1= i
            elif self.individuos[i].idade > self.individuos[maxIdade2].idade:
                maxIdade2= i
        self.maisVelho= self.individuos[maxIdade1].idade
        return (maxIdade1, maxIdade2)
    
    def getMaisNovo(self):
        menor= 0
        for i in range(0, tamPopulacao):
            if self.individuos[i].idade < self.individuos[menor].idade:
                menor= i
        return menor
    
    def getMaisVelhos(self):
        lista= []
        menor= self.getMaisNovo()
        maior= menor
        for j in range(0, math.floor(tamPopulacao/2)):
            for i in range(0, tamPopulacao):
                if self.individuos[i].idade > self.individuos[maior].idade and not i in lista:
                    maior= i
            lista.append(maior)
            maior= menor
        return lista
    
    def getMenosAdaptados(self):
        lista= []
        maior= self.individuos.index(self.getMaisAdaptado())
        menor= maior
        for j in range(0, math.floor(tamPopulacao/2)):
            for i in range(0, tamPopulacao):
                if self.individuos[i].adaptacao < self.individuos[menor].adaptacao and not i in lista:
                    menor= i
            lista.append(menor)
            menor= maior
        return lista
    
    def calculaAdaptacao(self):
        for i in range(tamPopulacao):
            self.individuos[i].calculaAdaptacao()
        self.getMaisAdaptado()  
        
    def envelhece(self):
        for i in range(tamPopulacao):
            self.individuos[i].idade= self.individuos[i].idade + 1

class AG:
    def __init__(self):
        self.populacao= Populacao()
        self.geracaoAtual= 0
        
    def selecao(self):
        soma= 0
        listaPontos= []
        for i in range(0, tamPopulacao):
            soma= soma + self.populacao.individuos[i].adaptacao
        for i in range(0, math.floor(tamPopulacao/2)):
            ponto= random.random()#*tamPopulacao
            #while ponto > soma:
            #    ponto= random.random()*tamPopulacao
            listaPontos.append(ponto)
            
        listaPais= []
        for k in range(0,math.floor(tamPopulacao/2)):
            p= 0
            i= 0
            pai= -1
            while p < ponto:
                p= p + self.populacao.individuos[i].adaptacao/soma
                if any(p >= j for j in listaPontos) and not i in listaPais:
                    pai= i
                elif any(p >= j for j in listaPontos) and i in listaPais:
                    k= k-1
                    continue
                i= i+1
            listaPais.append(pai)
        self.filhos= []
        for i in range(0, math.floor(tamPopulacao/2)):
            self.filhos.append(self.populacao.individuos[listaPais[i]].copy())
    
    def crossover(self):
        if random.random()>0.96:
            return
        for n in range(0, math.floor(tamPopulacao/2), 2):
            temp1= []
            temp2= []
            ponto1= random.randint(0, math.floor(tamGenes/2))
            ponto2= random.randint(math.floor(tamGenes/2), tamGenes)
            for i in range(ponto1, ponto2):
                temp1.append(self.filhos[n].genes[i])
            k= 0
            for i in range(0, tamGenes):
                flag= 0
                for j in range(0, ponto2-ponto1):
                    #print(n, i, j, k, "-", tamPopulacao/2, tamGenes, ponto1, ponto2, len(self.filhos))
                    if self.filhos[n+1].genes[i].nome == temp1[j].nome:
                        flag= 1
                if flag < 1:
                    temp2.append(self.filhos[n+1].genes[i])
                else:
                    self.filhos[n+1].genes[i]= temp1[k]
                    k= k+1
            k= 0
            for i in range(0, ponto1):
                self.filhos[n].genes[i]= temp2[k]
                k= k+1
            for i in range(ponto2, tamGenes):
                self.filhos[n].genes[i]= temp2[k]
                k= k+1
        
    def mutacao(self):
        for n in range(0, math.floor(tamPopulacao/2)):
            ponto1= random.randint(0, tamGenes)
            ponto2= random.randint(0, tamGenes)
            if ponto2>ponto1:
                ponto1, ponto2= ponto2,ponto1
            if tamPopulacao > 99:
                chance= 0.99
            #elif tamPopulacao < 40:
             #   chance= 0.4
            else:
                chance= tamPopulacao/100
                #chance= 0.8
            mutacao= random.random() > chance #1 - 1/math.log(tamPopulacao)
            if mutacao:
                aux= []
                for j in range(ponto1-ponto2):
                    aux.append(self.filhos[n].genes[ponto2+j])
                random.shuffle(aux)
                for j in range(ponto1-ponto2):
                    self.filhos[n].genes[ponto2+j]= aux[j]
    
    def mortalidade(self):
        mortos= []
        ponto= math.floor(tamPopulacao/2)
        velhos= self.populacao.getMaisVelhos()
        minimos= self.populacao.getMenosAdaptados()
        for i in range(0, math.floor(tamPopulacao/2)):
            if self.populacao.individuos[velhos[i]].idade > tamPopulacao:
                mortos.append(velhos[i])
            else:
                ponto= i
                break
        for i in range(0, math.floor(tamPopulacao/2) - ponto):
            mortos.append(minimos[i])
        #subtracao = [item for item in range(0, tamPopulacao) if item not in mortos]
        #for i in subtracao:
        #    if self.populacao.individuos[i].adaptacao < self.populacao.getMaisAdaptado().adaptacao:
        #        return mortos
        #for i in mortos:
        #    if self.populacao.individuos[i].adaptacao < self.populacao.getMaisAdaptado().adaptacao:
        #        mortos.remove(i)
                
        return mortos
    
    def adicionaFilhosMaisAdaptados(self):
        mortos= self.mortalidade()
        for i in range(0, math.floor(tamPopulacao/2)):
            self.filhos[i].calculaAdaptacao()
            self.populacao.individuos[mortos[i]]= self.filhos[i].copy()
            self.populacao.individuos[mortos[i]].idade= 0
    

def inicializaCartesiano():    
    grafo= GrafoCartesiano()
    with open("input1.txt", "r") as arquivo:
        i= 0
        for linha in arquivo:
            coords1= linha.split(",")
            coords= (float(coords1[0]), float(coords1[1]))
            grafo.add(Vertice(i, coords))
            i= i+1
    return grafo
    

grafo= inicializaCartesiano()
listaResults= []
listaMaximos= []
tamGenes= len(grafo.vertices)
tamPopulacao= 2* math.floor(math.pow(math.log(tamGenes), 2))

if math.floor(tamPopulacao/2) % 2 > 0 :
    tamPopulacao= tamPopulacao+2
#mutacao= (1 - (1/(math.log(tamGenes))))
for n in range(0, 1):
    demo= AG()
    demo.populacao.inicializaPopulacao(grafo)
    demo.populacao.calculaAdaptacao()
    #print("Geracao: ", demo.geracaoAtual, "- Mais Adaptado: ", demo.populacao.maisAdaptado)
    maior= demo.populacao.getMaisAdaptado().adaptacao
    genes= demo.populacao.getMaisAdaptado().genes
    numGeracoes = 20*math.floor(math.pow(tamPopulacao, 2.7))
    #if numGeracoes > 200000:
    #    numGeracoes= 200000
    #numGeracoes= 10000
    for i in range(0, numGeracoes):
    #while demo.populacao.getMaisAdaptado().adaptacao < 0.0095 :# or demo.geracaoAtual < 1500:
        demo.geracaoAtual= demo.geracaoAtual+1
        demo.populacao.envelhece()
        #print("Envelheceu -", i)
        demo.selecao()
        #print("Selecionou -", i)
        demo.crossover()
        #print("Crossover -", i)
        demo.mutacao()
        #print("Mutação -", i)
        demo.adicionaFilhosMaisAdaptados()
        #print("Adicionou filhos -", i)
        demo.populacao.calculaAdaptacao()
        #print("Calculou adaptação -", i)
        #print("Geracao: ", demo.geracaoAtual, "- Mais Adaptado: ", demo.populacao.maisAdaptado, "- Maior até agora: ", maior)
        if demo.populacao.getMaisAdaptado().adaptacao > maior:
            maior= demo.populacao.getMaisAdaptado().adaptacao
            genes= demo.populacao.getMaisAdaptado().genes
    listaResults.append(demo.populacao.getMaisAdaptado().adaptacao)
    listaMaximos.append(maior)
    #print("Solucao final na geracao ", demo.geracaoAtual)    
    print(n, "- Adaptacao: ",demo.populacao.getMaisAdaptado().adaptacao, "Custo:", 1/demo.populacao.getMaisAdaptado().adaptacao)
    #print("Genes: ")
    #for i in range(tamGenes):
    #    print(demo.populacao.getMaisAdaptado().genes[i])
    #print("Genes do mais adaptado: ")
    #for i in range(tamGenes):
    #    print(genes[i])
        
#plt.plot(range(0,30), listaResults, 'bo', range(0,30), listaMaximos, 'k')

    #8,2,3,9,4,1,6,0,5,7  -  0.01056... - 95.65