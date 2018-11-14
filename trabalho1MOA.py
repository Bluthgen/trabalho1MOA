# -*- coding: utf-8 -*-

import math
import random

class Vertice:
    def __init__(self, nome:int, coords:tuple):
        self.nome= nome
        self.x, self.y= coords

    @staticmethod
    def distance(v1, v2):
        return math.hypot(v2.x - v1.x, v2.y - v1.y)
    
    def __repr__(self):
        return f'{self.nome}'

class Grafo:
    def __init__(self):
        self.vertices= []
        
    def add(self, v):
        if isinstance(v, Vertice):
            self.vertices.append(v)
    
   # @property
   # def vertices(self):
   #     return self._vertices
    
    
class Individuo:
    def __init__(self):
        self.genes= []
        self.tamGenes= 10
        self.idade= 0
        #for i in range(self.tamGenes):
            #self.genes.append(Vertice(i, (random.random()*50, random.random()*50)))
        self.genes= [Vertice(0, (13.799940281434441 ,  44.703335320869506)), Vertice(1, (4.929969173873872 ,  38.57085858780106)), Vertice(2, (13.272217821147253 ,  14.380034596293035)), Vertice(3, (12.886353710138925 ,  14.516591138225692)), Vertice(4, (4.637545238897739 ,  29.0476235222785)), Vertice(5, (26.704681673223963 ,  35.54304838007247)), Vertice(6, (10.31369713595877 ,  37.18167173541928)), Vertice(7, (40.86283402907582 ,  31.63313651370869)), Vertice(8, (35.686213695624595 ,  7.532421945058254)), Vertice(9, (5.472325177881782 ,  25.33350450976665))]
        random.shuffle(self.genes)
        self._adaptacao= 0
    
    def calculaAdaptacao(self):
        self.adaptacao= 0
        peso= 0
        for i in range(self.tamGenes - 1):
            peso= peso + Vertice.distance(self.genes[i],self.genes[i+1])
        self.adaptacao= 1/peso
        
    def copy(self):
        copia= Individuo()
        copia.genes= self.genes.copy()
        copia.idade= self.idade
        copia.adaptacao= self.adaptacao
        return copia
        
class Populacao:
    def __init__(self):
        self.tamPopulacao= 20
        self.individuos= []
        self.maisAdaptado= 0
        
    def inicializaPopulacao(self):
        for i in range(self.tamPopulacao):
            self.individuos.append(Individuo())
        
    def getMaisAdaptado(self):
        maxAdapt= -1
        maxAdaptIndice= 0
        for i in range(self.tamPopulacao):
            if maxAdapt <= self.individuos[i].adaptacao:
                maxAdapt= self.individuos[i].adaptacao
                maxAdaptIndice= i
        self.maisAdaptado= self.individuos[maxAdaptIndice].adaptacao
        return self.individuos[maxAdaptIndice]
    
    def getSegundoMaisAdaptado(self):
        maxAdapt1= 0
        maxAdapt2= 0
        for i in range(self.tamPopulacao):
            if self.individuos[i].adaptacao > self.individuos[maxAdapt1].adaptacao:
                maxAdapt2= maxAdapt1
                maxAdapt1= i
            elif self.individuos[i].adaptacao > self.individuos[maxAdapt2].adaptacao:
                maxAdapt2= i
        return self.individuos[maxAdapt2]
    
    def getMenosAdaptados(self):
        minAdapt1= 0
        minAdapt2= 0
        for i in range(self.tamPopulacao):
            if self.individuos[minAdapt1].adaptacao >= self.individuos[i].adaptacao:
                minAdapt2= minAdapt1
                minAdapt1= i
            elif self.individuos[minAdapt2].adaptacao >= self.individuos[i].adaptacao:
                minAdapt2= i
        return (minAdapt1, minAdapt2)
    
    def getMaisVelhos(self):
        maxIdade1= 0
        maxIdade2= 0
        for i in range(self.tamPopulacao):
            if self.individuos[i].idade > self.individuos[maxIdade1].idade:
                maxIdade2= maxIdade1
                maxIdade1= i
            elif self.individuos[i].idade > self.individuos[maxIdade2].idade:
                maxIdade2= i
        self.maisVelho= self.individuos[maxIdade1].idade
        return (maxIdade1, maxIdade2)
    
    def calculaAdaptacao(self):
        for i in range(self.tamPopulacao):
            self.individuos[i].calculaAdaptacao()
        self.getMaisAdaptado()  
        
    def envelhece(self):
        for i in range(self.tamPopulacao):
            self.individuos[i].idade= self.individuos[i].idade + 1

class AG:
    def __init__(self):
        self.populacao= Populacao()
        self.geracaoAtual= 0
        
    def selecao(self):
        soma= 0
        for i in range(0, self.populacao.tamPopulacao):
            soma= soma + self.populacao.individuos[i].adaptacao
        ponto1= random.random()*self.populacao.tamPopulacao
        while ponto1 > soma:
            ponto1= random.random()*self.populacao.tamPopulacao
        ponto2= random.random()*self.populacao.tamPopulacao
        while ponto2 > soma:
            ponto2= random.random()*self.populacao.tamPopulacao
        p= 0
        i= 0
        adaptacaoAnt= 0
        pai1= -1
        pai2= -1
        while p < ponto1 or p < ponto2:
            pAnt= p
            p= p + self.populacao.individuos[i].adaptacao
            if p >= ponto1 and pAnt < ponto1:
                pai1= i
            if p >= ponto2 and pAnt < ponto2:
                if pai1 != i:
                    pai2= i
                else:
                    pAnt= pAnt - adaptacaoAnt
            adaptacaoAnt= self.populacao.individuos[i].adaptacao
            i= i+1
        
        self.filho1= self.populacao.individuos[pai1].copy()
        self.filho2= self.populacao.individuos[pai2].copy()
    
    def crossover(self):
        if random.random()>0.96:
            return
        temp1= []
        temp2= []
        ponto1= random.randint(0, self.populacao.individuos[0].tamGenes/2)
        ponto2= random.randint(self.populacao.individuos[0].tamGenes/2, self.populacao.individuos[0].tamGenes)
        for i in range(ponto1, ponto2):
            temp1.append(self.filho1.genes[i])
        k= 0
        for i in range(0, self.populacao.individuos[0].tamGenes):
            flag= 0
            for j in range(0, ponto2-ponto1):
                if self.filho2.genes[i].nome == temp1[j].nome:
                    flag= 1
            if flag < 1:
                temp2.append(self.filho2.genes[i])
            else:
                self.filho2.genes[i]= temp1[k]
                k= k+1
        k= 0
        for i in range(0, ponto1):
            self.filho1.genes[i]= temp2[k]
            k= k+1
        for i in range(ponto2, self.populacao.individuos[0].tamGenes):
            self.filho1.genes[i]= temp2[k]
            k= k+1
        
    def mutacao(self):
        ponto1= random.randint(0, self.populacao.individuos[0].tamGenes)
        ponto2= random.randint(0, self.populacao.individuos[0].tamGenes)
        if ponto2>ponto1:
            ponto1, ponto2= ponto2,ponto1
        mutacao= random.random()>0.78
        if mutacao:
            aux= []
            for j in range(ponto1-ponto2):
                aux.append(self.filho1.genes[ponto2+j])
            random.shuffle(aux)
            for j in range(ponto1-ponto2):
                self.filho1.genes[ponto2+j]= aux[j]
        
        ponto1= random.randint(0, self.populacao.individuos[0].tamGenes)
        ponto2= random.randint(0, self.populacao.individuos[0].tamGenes)
        if ponto2>ponto1:
            ponto1,ponto2= ponto2,ponto1
        mutacao= random.random()>0.78
        if mutacao:
            aux= []
            for j in range(ponto1-ponto2):
                aux.append(self.filho2.genes[ponto2+j])
            random.shuffle(aux)
            for j in range(ponto1-ponto2):
                self.filho2.genes[ponto2+j]= aux[j]
    
    def mortalidade(self):
        velhos= self.populacao.getMaisVelhos()
        minimos= self.populacao.getMenosAdaptados()
        if self.populacao.individuos[velhos[0]].idade > 15:
            morto1= velhos[0]
        else:
            morto1= minimos[0]
        if self.populacao.individuos[velhos[1]].idade > 15:
            morto2= velhos[1]
        elif morto1 == minimos[0]:
            morto2= minimos[1]
        else:
            morto2= minimos[0]
        return (morto1, morto2)
    
    def adicionaFilhosMaisAdaptados(self):
        self.filho1.calculaAdaptacao()
        self.filho2.calculaAdaptacao()
        mortos= self.mortalidade()
        self.populacao.individuos[mortos[0]]= self.filho1.copy()
        self.populacao.individuos[mortos[0]].idade= 0
        self.populacao.individuos[mortos[1]]= self.filho2.copy()
        self.populacao.individuos[mortos[1]].idade= 0
    
demo= AG()
demo.populacao.inicializaPopulacao()
demo.populacao.calculaAdaptacao()
print("Geracao: ", demo.geracaoAtual, "- Mais Adaptado: ", demo.populacao.maisAdaptado)
maior= demo.populacao.getMaisAdaptado().adaptacao
genes= demo.populacao.getMaisAdaptado().genes
for i in range(1500):
#while demo.populacao.getMaisAdaptado().adaptacao < 0.0095 or demo.geracaoAtual < 100:
    demo.geracaoAtual= demo.geracaoAtual+1
    demo.populacao.envelhece()
    demo.selecao()
    demo.crossover()
    demo.mutacao()
    demo.adicionaFilhosMaisAdaptados()
    demo.populacao.calculaAdaptacao()
    print("Geracao: ", demo.geracaoAtual, "- Mais Adaptado: ", demo.populacao.maisAdaptado, "- Maior até agora: ", maior, "Menor custo:", 1/maior)
    if demo.populacao.getMaisAdaptado().adaptacao > maior:
        maior= demo.populacao.getMaisAdaptado().adaptacao
        genes= demo.populacao.getMaisAdaptado().genes
print("Solucao final na geracao ", demo.geracaoAtual)    
print("Adaptacao: ",demo.populacao.getMaisAdaptado().adaptacao, "Custo:", 1/demo.populacao.getMaisAdaptado().adaptacao)
print("Genes: ")
for i in range(demo.populacao.individuos[0].tamGenes):
    print(demo.populacao.getMaisAdaptado().genes[i])
print("Genes do mais adaptado: ")
for i in range(demo.populacao.individuos[0].tamGenes):
    print(genes[i])
    
    #9,5,6,8,0,1,4,7,2,3  -  0.0094