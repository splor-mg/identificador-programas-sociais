#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from  math import ceil
from dataclasses import dataclass

def get_ano(base):
    
    return int(base['Ano Monitoramento'].unique())

def get_mes_inicial(base):
    
    return int(base['Mês Inicial'].unique())

def get_mes_final(base):
    
    return int(base['Mês Final'].unique())



@dataclass
class Grupos:
    """Class for store groups of id and its names for use in the the tests methods."""
    name : str
    index : []
    values : [list]   


class Constants: #classe para simular uma struct (sim, eu sei...)
    pass

    def __init__(self, base_acoes, base_loc):
        
        
        self.ANO_MON = get_ano(base_acoes)
        self.MES_INICIAL = get_mes_inicial(base_acoes)
        self.MES_FINAL = get_mes_final(base_acoes)
        
        # ??? NECESSARIO VER SE acoes_mon SEMPRE TERÁ TODAS AS ACOES POSSIVEIS ???
        self.ACOES_NAO_ORC = Grupos('Ações Não-Orçamentárias',
                                    'Código da Ação',
            list(base_acoes[base_acoes['Código da Ação'].astype(str).str.startswith('5')]['Código da Ação'])
                                   )
        
        self.TODAS_ACOES = Grupos('Todas as Ações',
                                  'Código da Ação',
                                  list(base_acoes['Código da Ação'])
                                 )
                            
        
        self.EMPRESAS_INDEPENDENTES = Grupos("Empresas Independentes",
                                             'Código da Unidade Orçamentária Responsável pela Ação',
                                             list(base_acoes[base_acoes['Código da Unidade Orçamentária Responsável pela Ação']
                                             .astype(str).str.startswith('5')]['Código da Unidade Orçamentária Responsável pela Ação'])
                                            )
    
        self.ACOES_UOS_EXCECAO = Grupos( "Ações e UOs de Exceção",
                                        ['Código da Ação','Código da Unidade Orçamentária Responsável pela Ação'],
                                        [(7007, 1251), (7007, 1401), (7024, 1941), (7441, 1941),(7002, 2121),(2065, 1261),(2066, 1261) ])

        self.OUTROS_PODERES = Grupos( 'UOs de Outros Poderes', 
                                     'Código da Unidade Orçamentária Responsável pela Ação',
                                         [1011, 1021, 1031,1051,1091,1441, 2361, 4031, 4121, 4441, 4451, 4611, 4711]
                                        )
        
        self.ACOES_CUMULATIVAS = Grupos( 'Ações com Metas Cumulativas',
                                        ['Código da Ação','Código da Unidade Orçamentária Responsável pela Ação'],
                                        list(base_acoes[base_acoes['Meta não cumulativa?'] == 'NÃO']                                     [['Código da Ação', 'Código da Unidade Orçamentária Responsável pela Ação']].apply(tuple, axis=1))
                                       )
        
        self.ACOES_NÃO_CUMULATIVAS = Grupos( 'Ações com Metas Cumulativas',
                                        ['Código da Ação','Código da Unidade Orçamentária Responsável pela Ação'],
                                        list(base_acoes[base_acoes['Meta não cumulativa?'] == 'SIM']                                     [['Código da Ação', 'Código da Unidade Orçamentária Responsável pela Ação']].apply(tuple, axis=1))
                                       )
                                        
        
            
        self.ABREV_MES = {1: 'Jan', 2: 'Fev', 3 : 'Mar' , 4 : 'Abr' , 5 : 'Mai' , 6 : 'Jun' , 7 : 'Jul' , 8 : 'Ago' , 9 : 'Set' , 
                          10 : 'Out' , 11 : 'Nov' , 12 : 'Dez'}    
        
        self.COLUNAS_AGREGADO = ['Código da Ação', 'Código da Unidade Orçamentária Responsável pela Ação']

        self.am_mesInicial = int(base_acoes['Mês Inicial'].unique())
        self.am_mesFinal = int(base_acoes['Mês Final'].unique())
        self.lm_mesInicial = int(base_loc['Mês Inicial'].unique())
        self.lm_mesFinal = int(base_loc['Mês Final'].unique())
        self.am_ano = int(base_acoes['Ano Monitoramento'].unique())
        self.lm_ano = int(base_loc['Ano Monitoramento'].unique())





#define constantes baseadas nas bases para uso no escopo deste módulo. É chamada em normaliza_bases()
def cria_constantes(base_acoes, base_mon): 
    global const
    const = Constants(base_acoes, base_mon)
    
    return const
            
# usar como name(var=var) para retornar o nome da variavel, não funciona com as const       
def name(**variables):
    r =  [x for x in variables]
    return f"{r}"



#__________________________________________________________________________________________________________________________________________


def load_bases_sigplan(diretorio, nome_arquivo):  
    
    df = pd.read_csv(diretorio + nome_arquivo, delimiter='|', encoding='latin-1', decimal=',')
    df.name = nome_arquivo
    df.index.name = 'row_number'
    
    #limpar colunas totalmente vazias
    df.dropna(axis='columns', how='all', inplace=True)
    
    return df


def load_bases_siafi(diretorio, nome_planilha):

    #falta ver se coloca NaN = 0 e como fazer isso
    df = pd.read_excel(diretorio + nome_planilha, skip_blank_lines=True ).fillna(0)
    df.name = nome_planilha
    df.index.name = 'row_number'
    
    
    return df

def load_bases_sisor(diretorio, nome_planilha):

    #falta ver se coloca NaN = 0 e como fazer isso
    df = pd.read_excel(diretorio + nome_planilha, skip_blank_lines=True ).fillna(0)
    df.name = nome_planilha
    df.index.name = 'row_number'
    
    
    return df



def valida_bases_sigplan(base_acoes, base_loc):
   
    cria_constantes(base_acoes, base_loc)
    
    print('Verificando se as bases são de períodos das bases equivalentes (Mês e Ano):')
   
    if (const.am_mesInicial == const.lm_mesInicial) & (const.am_mesFinal == const.lm_mesFinal) & (const.am_ano == const.lm_ano):
        print('Sucesso.')

        return True

    else:
       
        print('Falha. Bases acoes e localizadores não são de períodos equivalentes.')
        return False

    
def valida_bases_siafi(exec_sigplan, invest_sigplan):
    
    #conferir os meses entre acoes e locMon e bases siafi?
    pass
    
    

def init_base_sigplan(base_sigplan):       
    
    #valida_bases_sigplan(base_sigplan, base_loc)
    
    #Normalização de nomes de colunas
    base_sigplan.columns = base_sigplan.columns.str.replace('Desp.','Despesa', regex=False)



    base_sigplan.columns = base_sigplan.columns.str.replace('Fis ','Físico ', regex=False)
    

    #base_sigplan.columns = base_sigplan.columns.str.replace('Realização Física ' +str(const.ANO_MON),'Físico Realizado ' +str(const.ANO_MON))

    
    #retira espaços duplos dos nomes das colunas
    
    base_sigplan.columns = base_sigplan.columns.str.replace('\s+', '_', regex=True)
    base_sigplan.columns = map(str.lower, base_sigplan.columns)


    
def init_bases_siafi(exe_siafi, inv_siafi):
    
    
    mes_final = exe_siafi.columns[-1] # pega ultima coluna da tabela, que indica o ultimo mes do relatório
    
    exe_siafi.columns = exe_siafi.columns.map(lambda x: 'Despesa Realizada ' + str(const.ABREV_MES[x]) if isinstance(x, int) else x )
    
    inv_siafi.columns = inv_siafi.columns.map(lambda x: 'Despesa Realizada Investimento ' + str(const.ABREV_MES[x]) if isinstance(x, int) else x )
    


    
#_________________________________________________________________________________________________________________________________________

def get_subset_dataframe(variavel, base, fuzzy=False):
    
    if variavel.lower() == 'despesa realizada':        
        return base.filter(regex='Desp.*\s.*Realizada+ (\w{3}$|\d{4})')

    elif variavel.lower() == 'despesa realizada 2020':
        return base.filter(regex='Despesa Realizada 2020')
    
    elif variavel.lower() == 'físico realizado':
        return base.filter(regex='(Físico R.*|Realização\sF.*)')
    
    
    elif variavel.lower() == 'pessoa remunerada':
        return base.filter(regex='(Pessoa\sR.*|Realização\sP.*)')
     

    elif variavel.lower() == 'despesa discriminada':
        return base.filter(regex='Desp.*\s.*Realizada')
 
    
    elif variavel.lower() == 'despesa programada':
        return base.filter(regex='Prog.+Desp')
     
    
    elif variavel.lower() == 'orçamento':
        return base.filter(regex='Orç*')
    
    
    elif variavel.lower() in ('crédito autorizado', 'credito autorizado', 'loa + créditos', 'loa + creditos',
                              'crédito autorizado 2020 (loa + créditos)', 'crédito autorizado (loa + créditos)'):
        return base.filter(regex='Crédito Autorizado*')
    
    
    elif variavel.lower() in ('programação inicial desp. pessoal e auxílios', 'despesa pessoal', 
                              'programação inicial despesa pessoal e auxílios', 'despesa realizada pessoal e auxílios', 
                              'prog. inicial desp. pessoal e auxílios'):
        
        return base.filter(regex='(Despesa Pessoal|Despesa+.*Pessoal)+')
    
    
    elif variavel.lower() in ('prog. inicial outras desp.', 'despesa outros', 'outras despesas', 
                              'prog. inicial outras despesa', 'programação inicial outras despesa', 
                              'programação inicial outras desp.', 'despesa realizada outros'):
        
        return base.filter(regex='(Outras Despesa|Despesa+.*Outros)+')
    
    
    else:
        print('Nome de grupo de colunas não encontrado.')
        return pd.DataFrame()
    

def get_nomes_colunas_regex(variavel, base, fuzzy=False):
    
    # Despesa Realizada
    if variavel.lower() == 'despesa realizada':        
        return base.filter(regex='Desp.*\s.*Realizada+ (\w{3}$|\d{4})').columns.format()

    elif variavel.lower() == 'despesa realizada ano':
        return base.filter(regex='Despesa Realizada \d{4}').columns.format()
    
    elif variavel.lower() == 'despesa realizada mês':
        return base.filter(regex='Despesa Realizada \D{3}$').columns.format()
    
    
    # Fisico Realizado
    elif variavel.lower() == 'físico realizado':
        return base.filter(regex='(Físico R.*|Realização\sF.*)').columns.format()
    
    elif variavel.lower() == 'físico realizado mês':
        return base.filter(regex='(Físico R.* \D{3}$)').columns.format()
    
    elif variavel.lower() == 'físico realizado ano':
        return base.filter(regex='(Físico R.* \d{4}|Realização\sF.*)').columns.format()
    
    
    # Pessoa Remunerada
    elif variavel.lower() == 'pessoa remunerada':
        return base.filter(regex='(Pessoa\sR.*|Realização\sP.*)').columns.format()
    
    elif variavel.lower() == 'pessoa remunerada mês':
        return base.filter(regex='(Pessoa\sR.* \D{3}$)').columns.format()
    
    elif variavel.lower() == 'pessoa remunerada ano':
        return base.filter(regex='(Pessoa\sR.* \d{4}$|Realização\sP.*)').columns.format()
    
    
    # Despesa Realizada com suas subdivisões
    elif variavel.lower() == 'despesa discriminada':
        return base.filter(regex='Desp.*\s.*Realizada').columns.format()
 
    elif variavel.lower() == 'despesa discriminada mês':
        return base.filter(regex='Desp.*\s.*Realizada.* \D{3}$').columns.format()

    elif variavel.lower() == 'despesa discriminada ano':
        return base.filter(regex='Desp.*\s.*Realizada.* \d{4}$').columns.format()
    
    
    # Despesa Realizada Investimento Somente
    elif variavel.lower() in ('despesa realizada investimento', 'despesa investimento'):
        return base.filter(regex='(Despesa+.*Investimento+.*|Desp+.*Invest+)').columns.format()
    
    elif variavel.lower() in ('despesa realizada investimento mês', 'despesa investimento mês', 'despesa realizada investimento mes'):
        return base.filter(regex='(Despesa+.*Investimento+.*\D{3}$|Desp+.*Invest+\D{3}$)').columns.format()
    
    elif variavel.lower() in ('despesa realizada investimento ano', 'despesa investimento ano'):
        return base.filter(regex='(Despesa+.*Investimento+.*\d{4}$|Desp+.*Investimento+\d{4}$)').columns.format()
    
    
    # Despesa Realizada Pessoal Somente
    elif variavel.lower() in ('despesa realizada pessoal', 'despesa pessoal'):
        return base.filter(regex='(Despesa+.*Pessoal+.*|Desp+.*Pessoal+)').columns.format()
    
    elif variavel.lower() in ('despesa realizada pessoal mês', 'despesa pessoal mês', 'despesa realizada pessoal mes'):
        return base.filter(regex='(Despesa+.*Pessoal+.*\D{3}$|Desp+.*Pessoal+\D{3}$)').columns.format()
    
    elif variavel.lower() in ('despesa realizada pessoal ano', 'despesa pessoal ano'):
        return base.filter(regex='(Despesa+.*Pessoal+.*\d{4}$|Desp+.*Pessoal+\d{4}$)').columns.format()
    
    
    # Despesa Realizada Outros Somente
    elif variavel.lower() in ('despesa realizada outros', 'despesa outros'):
        return base.filter(regex='(Despesa+.*Outros+)').columns.format()
    
    elif variavel.lower() in ('despesa realizada outros mês', 'despesa outros mês', 'despesa realizada outros mes'):
        return base.filter(regex='(Despesa+.*Outros+.*\D{3}$|Desp+.*Outros+\D{3}$)').columns.format()
    
    elif variavel.lower() in ('despesa realizada outros ano', 'despesa outros ano'):
        return base.filter(regex='(Despesa+.*Outros+.*\d{4}$|Desp+.*Outros+\d{4}$)').columns.format()
     
    
    # Programação Inicial de Despesa
    elif variavel.lower() in ('programação inicial de despesa'):
        return base.filter(regex='Prog.+Desp').columns.format()
 
    elif variavel.lower() in ('programação inicial de despesa mês'):
        return base.filter(regex='Prog.+Desp.* \D{3}$').columns.format()
                              
    elif variavel.lower() in ('programação inicial de despesa ano'):
        return base.filter(regex='Total.+Prog.+Inicial.+').columns.format()
    
    
    # Programação Inicial de Outras Despesa
    elif variavel.lower() in ('programação inicial de outras despesas'):
        return base.filter(regex='Prog.+Outras.+Desp.+').columns.format()
 
    elif variavel.lower() in ('programação inicial de outras despesas mês'):
        return base.filter(regex='Prog.+Outras.+Desp.*\s\D{3}$').columns.format()
                              
    elif variavel.lower() in ('programação inicial de outras despesas ano'):
        return base.filter(regex='Total.+Prog.+Inicial.+Outras').columns.format()
    
    
    # Programação Inicial de Despesa de Pessoal e Auxílios
    elif variavel.lower() in ('programação inicial de despesa de pessoal'):
        return base.filter(regex='Prog.+Desp.+Pessoal.+').columns.format()
    
    elif variavel.lower() in ('programação inicial de despesa de pessoal mês'):
        return base.filter(regex='Prog.+Desp.+Pessoal.*\s\D{3}$').columns.format()
    
    elif variavel.lower() in ('programação inicial de despesa de pessoal ano'):
        return base.filter(regex='Total.+Prog.+Inicial.+Pessoal.*').columns.format()
    
    # Orçamento
    elif variavel.lower() == 'orçamento ano':
        return base.filter(regex='(Previsão Orç|Orç. Progra)').columns.format()
    
    elif variavel.lower() in('previsão orçamentária ano', 'previsão orçamentária'):
        return base.filter(regex='Previsão.+Orç.+').columns.format()
    
    elif variavel.lower() in ('orçamento programado ano', 'orçamento programado'):
        return base.filter(regex='Orç.+Programad.+').columns.format()
    
    
    
    
    
    
    
    #legado --------
    
    elif variavel.lower() in ('despesa programada', 'programação de despesa'):
        return base.filter(regex='Prog.+Desp').columns.format()    
    
    elif variavel.lower() in ('físico programado', 'programação física', 'fisico programado', 'programacao fisica', 
                              'físico programado inicial', 'fisico programado inicial' ):
        return base.filter(regex='(Previ.+Fís.+|Fís.+Prog.+)').columns.format()
    
    elif variavel.lower() in ('meta física','meta fisica', 'meta física reprogramada', 'meta fisica reprogramada',
                              'físico reprogramado', 'fisico reprogramado', 'físico meta','fisico meta' ):
        return base.filter(regex='(Fís.+Reprog.+)').columns.format()

    

    
    
    elif variavel.lower() in ('crédito autorizado', 'credito autorizado', 'loa + créditos', 'loa + creditos',
                              'crédito autorizado 2020 (loa + créditos)', 'crédito autorizado (loa + créditos)'):
        return base.filter(regex='Crédito Autorizado*').columns.format()
    
    
    elif variavel.lower() in ('prog. inicial outras desp.', 'despesa outros', 'outras despesas', 
                          'prog. inicial outras despesa', 'programação inicial outras despesas', 
                          'programação inicial outras desp.', 'despesa realizada outros'):
        return base.filter(regex='(Outras Despesa|Despesa+.*Outros)+').columns.format()
    
    elif variavel.lower() in ('programação inicial desp. pessoal e auxílios', 'despesa pessoal', 
                              'programação inicial despesa pessoal e auxílios', 'despesa realizada pessoal e auxílios', 
                              'prog. inicial desp. pessoal e auxílios'):
        return base.filter(regex='(Despesa Pessoal|Despesa+.*Pessoal)+').columns.format()
    
    
    elif variavel.lower() in ('despesa investimento', 'desp. investimento', 'investimento', 
                              'despesa realizada investimento', 'desp. realizada investimento',
                              'desp. realizada invest.', 'desp. invest.'):
        return base.filter(regex='(Despesa Investimento|Desp+.*Invest)+').columns.format()
    
    
    else:
        print('Nome de grupo de colunas não encontrado.')
        return []
    


def get_coluna_byname(nome_coluna, dataframe): #colocar regex
    
    return dataframe[nome_coluna]


def filter_dataframe(variavel, lista_valores, dataframe):
    
    dataframe[variavel].isin(lista_valores)

    return df

def get_dict_agg(nome_colunas, nome_funcao, repeticoes):
    
    return dict(list(zip(nome_colunas,[nome_funcao]*repeticoes)))


def get_subset_rows(nome_index, base, lista_valores='all'):
    
    """
    | recebe uma lista de uma ou mais colunas e retorna um DF com a linhas filtradas pelo parametro lista_valores. 
    | Lista_colunas e lista_valores tem de ter dimensoes iguais.
     """
    
    #colocar depois try catch para tratamento de erro pra quando não achar a coluna buscar no index.
    temp = base.index.names
    base.reset_index(inplace=True)
      
    
    
    #APAGAR parece nao ser necessario
    if lista_valores == 'all':
        base.set_index(temp, inplace=True)
        return base 
    
    elif isinstance(nome_index, list): #se tiver mais de uma string (for lista)         
        
        #transforma e tuplas para buscar por indices simultaneamente
        r = base[base[nome_index].apply(tuple, axis=1).isin(list(map(tuple, lista_valores)) )] 
        r.set_index(temp, inplace=True)
        return r
                        
    else: #se for somente uma string como nome da coluna selecionada
        r = base[base[nome_index].isin(lista_valores)]
        r.set_index(temp, inplace=True)
        return r
      

def filter_df_by_grupo(grupo, base, exceto= False):
    
    """
    | recebe uma lista de uma ou mais colunas e retorna um DF com a linhas filtradas pelo parametro lista_valores. 
    | Lista_colunas e lista_valores tem de ter dimensoes iguais. Se exceto=True retorna linhas que não pertencem àquele grupo
     """
    if (exceto == True):
    
        if isinstance(grupo.index, list):
            r = base[~base.index.isin(grupo.values)]
        else:
            r = base[~base.index.get_level_values(grupo.index).isin(grupo.values)]

        return r    
    
    else:
        
        if isinstance(grupo.index, list):
            r = base.loc[grupo.values]
        else:
            r = base[base.index.get_level_values(grupo.index).isin(grupo.values)]

        return r


      
'''   
    #colocar depois try catch para tratamento de erro pra quando não achar a coluna buscar no index.
    temp = base.index.names
    base.reset_index(inplace=True)
      
    
    
    #APAGAR parece nao ser necessario
    if lista_valores == 'all':
        base.set_index(temp, inplace=True)
        return base 
    
    elif isinstance(nome_index, list): #se tiver mais de uma string (for lista)         
        
        #transforma e tuplas para buscar por indices simultaneamente
        r = base[base[nome_index].apply(tuple, axis=1).isin(list(map(tuple, lista_valores)) )] 
        r.set_index(temp, inplace=True)
        return r
                        
    else: #se for somente uma string como nome da coluna selecionada
        r = base[base[nome_index].isin(lista_valores)]
        r.set_index(temp, inplace=True)
        return r
       
'''
        
        
#__________________________________________________________________________________________________________________________________________
    
    
def teste_c1_igual_entre_bases(nome_colunas, base_1, base_2, grupo, exceto=False):

    print('\n\nTESTE:  Verifica nas bases \"' +base_1.name+ '\" e \"' +base_2.name+ '\" se as variáveis são iguais', 
          'exceto' if exceto == True else '', 'para '  +grupo.name+' \n')

    
    base_a = filter_df_by_grupo(grupo, base_1, exceto)
    base_b = filter_df_by_grupo(grupo, base_2, exceto)

    dict_agg = get_dict_agg(nome_colunas, 'sum', const.MES_FINAL)

    base_agg_a = base_a.groupby(const.COLUNAS_AGREGADO).agg(dict_agg)

    base_agg_b = base_b.groupby(const.COLUNAS_AGREGADO).agg(dict_agg)

    #df_merged = base_agg_a.merge(base_agg_b, left_index=True, right_index=True, how='outer',suffixes=('_a', '_b'))

    grp = round(base_agg_a.subtract(base_agg_b, level=None, fill_value=0),3)

    filtro = grp[nome_colunas[0:-1]] == 0

    for nome,resultado in zip(filtro.all().index, filtro.all().values):
        print('Coluna ['+nome+'] - ', 'Sucesso' if resultado == True else 'Falha')

    if filtro.all(1).all():
        print('\nNão foram encontradas divergências.')
    else:
        divergencias = grp[~filtro.all(1)]
        diretorio = 'Divergencias/'
        grava_csv(diretorio, 'Categoria 1 Grupo 1 - '+ base_1.name[0:-4] +' x ' + base_2.name[0:-5] , divergencias )



def teste_c2_igualmenor(nome_coluna1, nome_coluna2, base, agregar=True):

    print('\n\nTESTE:  Verifica na base \"' +base.name+ '\" se todos valores de', nome_coluna1,
          'são menores ou iguais aos valores de ',nome_coluna2,'.')

    #APAGAR - para testes
    #base.loc[0, nome_coluna1] = 999999999

    if agregar == True:

        indice_agg = const.COLUNAS_AGREGADO
        colunas_agg = nome_coluna1 + nome_coluna2

    else:
        base.reset_index(inplace=True)
        indice_agg = const.COLUNAS_AGREGADO

        colunas_agg = [nome_coluna1 , nome_coluna2]



    dict_agg = get_dict_agg(colunas_agg, 'sum', len(colunas_agg))

    grp = base.groupby(indice_agg).agg(dict_agg)


    filtro = grp[nome_coluna1].sum(axis=1).le(grp[nome_coluna2].sum(axis=1))

    if filtro.all():
        print('Sucesso.')
    else:
        print('Falha')
        divergencias = grp[filtro == False]
        diretorio = 'Divergencias/'
        grava_csv(diretorio, 'Grupo 2 - ['+nome_coluna1+'] M.E ['+nome_coluna2+']' , divergencias )


    
def teste_c3_colunas_iguais(nome_coluna1, nome_coluna2, base, agregar=False):

    print('\n\nTESTE:  Verifica na base \"' +base.name+ '\" se todos valores de ['+nome_coluna1+'] são iguais aos valores de ['+nome_coluna2+'].')

    #APAGAR - para testes
    #base.loc[0, nome_coluna1] = 999999999

    if agregar == True:
        indice_agg = const.COLUNAS_AGREGADO
        colunas_agg = [nome_coluna1 , nome_coluna2]

    else:
        indice_agg = [base.index.name] + const.COLUNAS_AGREGADO
        colunas_agg = [nome_coluna1 , nome_coluna2]



    dict_agg = get_dict_agg(colunas_agg, 'sum', len(colunas_agg))

    grp = base.groupby(indice_agg).agg(dict_agg)

    #nao arrendoda pois valores físicos são números inteiros.
    diff = grp[nome_coluna1].subtract(grp[nome_coluna2])

    filtro = grp[nome_coluna1].le(grp[nome_coluna2])

    if filtro.all():
        print('Sucesso.')
    else:
        print('Falha')
        divergencias = grp[filtro == False]
        diretorio = 'Divergencias/'
        grava_csv(diretorio, '/Divergencias Grupo 3 - ['+nome_coluna1+'] Eq ['+nome_coluna2+']' , divergencias )


def teste_c4_igual_zero(lista_colunas_testadas, grupo, base, agregar=True ):


    print('\n\nTESTE:  Verifica na base \"' +base.name+ '\" se todos valores são iguais a zero para '  +grupo.name+' \n')

    if agregar == True:
        indice_agg = const.COLUNAS_AGREGADO
        colunas_agg = lista_colunas_testadas

    else:
        indice_agg = [base.index.name] + const.COLUNAS_AGREGADO
        colunas_agg = lista_colunas_testadas



    dict_agg = get_dict_agg(colunas_agg, 'sum', len(colunas_agg))
    
    
    
    
    grp = base.groupby(indice_agg).agg(dict_agg)

    
    #grp.reset_index(inplace = True)

    #filtra o dataframe para a categoria de linhas desejada
    grp = filter_df_by_grupo(grupo, grp)



    filtro = grp[lista_colunas_testadas] == 0


    #imprime os resultados para cada coluna
    for nome,resultado in zip(filtro.all().index, filtro.all().values):
        print('Coluna ['+nome+'] - ', 'Sucesso' if resultado == True else 'Falha')

    if filtro.all(1).all():
        print('\nNão foram encontradas divergências.')
    else:
        divergencias = grp[~filtro.all(1)]
        diretorio = 'Divergencias/'
        grava_csv(diretorio, 'Cat 4 - ' + grupo.name + ' - Valores Diferentes de Zero - ' + base.name[0:-4] , divergencias )




def teste_c5_valores_positivos(lista_colunas_testadas, base, agregar=True, exceto=False ):


    print('\n\nTESTE:  Verifica na base \"' +base.name+ '\" se todos valores são maiores ou iguais a zero.\n')



    filtro = base[lista_colunas_testadas] >= 0


    #imprime os resultados para cada coluna
    for nome,resultado in zip(filtro.all().index, filtro.all().values):
        print('Coluna ['+nome+'] - ', 'Sucesso' if resultado == True else 'Falha')

    if filtro.all(1).all():
        print('\nNão foram encontradas divergências.')
    else:
        divergencias = grp[~filtro.all(1)]
        diretorio = 'Divergencias/'
        grava_csv(diretorio, 'cat 5 - Valores negativos - ' + base.name[0:-4] , divergencias )


#retirar      
# def teste_c6_somatorio_igual_coluna(colunas_somadas, coluna_total, base, grupo, agregar=True, exceto=False, separar_metas= False):

#     print('\n\nTESTE:  Verifica na base \"' +base.name+ '\" para ' +grupo.name+ ' se o valor da coluna ', coluna_total , 
#           'é igual ao somatório das colunas:\n' + '\n'.join(colunas_somadas))

#     #APAGAR - para testes
#     #base.loc[0, nome_coluna1] = 999999999

#     if agregar == True:

#         indice_agg = const.COLUNAS_AGREGADO
#         colunas_agg = colunas_somadas + coluna_total

#     else:
#         base.reset_index(inplace=True)
#         indice_agg = const.COLUNAS_AGREGADO

#         colunas_agg = nome_coluna1 + nome_coluna2



#     dict_agg = get_dict_agg(colunas_agg, 'sum', len(colunas_agg))

#     grp = base.groupby(indice_agg).agg(dict_agg)
    
#     #filtra para o grupo
#     grp = filter_df_by_grupo(grupo, grp)
    
#     if (separar_metas == False): #tratar fisico realizado e pessoa remunerada.

#         #subtrai as duas colunas para obter resultados esperado ( =0 )
#         diff = round(grp[coluna_total].sum(axis=1) - grp[colunas_somadas].sum(1),3)
#         filtro = diff == 0
        
#     else:
#         grp_cum = grp[grp['Meta não cumulativa?'] == 'NÃO']
#         grp_nao_cum = grp[grp['Meta não cumulativa?'] == 'SIM']
    
#         diff_cum = round(grp_cum[coluna_total].max(axis=1) - grp_cum[colunas_somadas].max(1),3)
#         diff_nao_cum = round(diff_nao_cum[coluna_total].sum(axis=1) - diff_nao_cum[colunas_somadas].sum(1),3)
    
#         frames = [diff_cum, diff_nao_cum]
#         diff = pd.concat(frames)
    
#         filtro = diff == 0


#     if filtro.all():
#         print('\nRESULT: Sucesso.')
#     else:
#         print('\nRESULT: Falha')
#         divergencias = grp[filtro == False]
#         nome_arquivo = 'Cat 6 - ' + str(*coluna_total)
#         grava_csv( nome_arquivo  , divergencias )

  
def teste_c6_somatorio_igual_coluna(colunas_somadas, coluna_total, base, grupo, agregar=True, exceto=False, metas_cumulativas='none'):
#metas_cumulativas 'none', 'split' ou 'all'


#  
# colunas_somadas = get_nomes_colunas_regex('Físico Realizado Mês', acoesMon)
# coluna_total = get_nomes_colunas_regex('Físico Realizado Ano', acoesMon)
# grupo = const.TODAS_ACOES
# base = acoesMon
# agregar=True
# exceto=False
# metas_cumulativas= 'all'
# coerce_meta_cumulativa=False


    print('\n\nTESTE:  Verifica na base \"' +base.name+ '\" para ' +grupo.name+ ' se o valor da coluna', coluna_total , 
          'é igual ao somatório das colunas:\n' + '\n'.join(colunas_somadas))

    #APAGAR - para testes
    #base.loc[0, nome_coluna1] = 999999999

    if agregar == True:

        indice_agg = const.COLUNAS_AGREGADO
        colunas_agg = colunas_somadas + coluna_total

    else:
        base.reset_index(inplace=True)
        indice_agg = const.COLUNAS_AGREGADO

        colunas_agg = nome_coluna1 + nome_coluna2



    if (metas_cumulativas == 'all'): #usar para pessoa remunerada somente, não misturar com outras colunas

        dict_agg = get_dict_agg(colunas_agg, 'sum', len(colunas_agg))

        grp = base.groupby(indice_agg).agg(dict_agg)

        #filtra para o grupo
        grp = filter_df_by_grupo(grupo, grp)


        #subtrai as duas colunas para obter resultados esperado ( =0 )
        diff = round(grp[coluna_total].max(axis=1) - grp[colunas_somadas].max(axis=1),3)

        filtro = diff == 0





    elif (metas_cumulativas == 'split'): #usar para físico realizado somente, não misturar com outras colunas

        base_cum = base[base['Meta não cumulativa?'] == 'NÃO']
        base_nao_cum = base[base['Meta não cumulativa?'] == 'SIM']

        dict_agg = get_dict_agg(colunas_agg, 'sum', len(colunas_agg))

        grp_cum = base_cum.groupby(indice_agg).agg(dict_agg)
        grp_nao_cum = base_nao_cum.groupby(indice_agg).agg(dict_agg)


        diff_cum = round(grp_cum[coluna_total].sum(axis=1) - grp_cum[colunas_somadas].sum(axis=1),3)
        diff_nao_cum = round(grp_nao_cum[coluna_total].max(axis=1) - grp_nao_cum[colunas_somadas].max(axis=1),3)

        frames = [diff_cum, diff_nao_cum]
        diff = pd.concat(frames)

        filtro = diff == 0

    else: #usar para quando não houver físico realizado ou pessoa remunerada nas colunas.

        dict_agg = get_dict_agg(colunas_agg, 'sum', len(colunas_agg))

        grp = base.groupby(indice_agg).agg(dict_agg)

        #filtra para o grupo
        grp = filter_df_by_grupo(grupo, grp)


        #subtrai as duas colunas para obter resultados esperado ( =0 )
        diff = round(grp[coluna_total].sum(axis=1) - grp[colunas_somadas].sum(1),3)
        filtro = diff == 0.000



    if filtro.all():
        print('\nRESULT: Sucesso.')
    else:
        print('\nRESULT: Falha')
        divergencias = grp[filtro == False]
        
        diretorio = 'Divergencias/'        
        nome_arquivo = 'Cat 6 - ' + str(*coluna_total)        
        
        grava_csv( nome_arquivo  , divergencias )

        
        
        
def teste_c7_somatorio_positivo(colunas_somadas, base, grupo, agregar=True, exceto=False, metas_cumulativas='none'):

    print('\n\nTESTE:  Verifica na base \"' +base.name+ '\" para ' +grupo.name+ ' se o somatório é positivo para as colunas:\n' + '\n'.join(colunas_somadas))


    if agregar == True:

        indice_agg = const.COLUNAS_AGREGADO
        colunas_agg = colunas_somadas

    else:
        base.reset_index(inplace=True)
        indice_agg = const.COLUNAS_AGREGADO

        colunas_agg = nome_coluna1 + nome_coluna2



    if (metas_cumulativas == 'all'): # Usar para pessoa remunerada somente, não misturar com outras colunas

        dict_agg = get_dict_agg(colunas_agg, 'sum', len(colunas_agg))

        grp = base.groupby(indice_agg).agg(dict_agg)

        #filtra para o grupo
        grp = filter_df_by_grupo(grupo, grp)


        #subtrai as duas colunas para obter resultados esperado ( =0 )
        somatorio = grp[colunas_somadas].max(axis=1)

        filtro = somatorio >= 0



    elif (metas_cumulativas == 'split'): # Usar para físico realizado somente, não misturar com outras colunas

        base_cum = base[base['Meta não cumulativa?'] == 'NÃO']
        base_nao_cum = base[base['Meta não cumulativa?'] == 'SIM']

        dict_agg = get_dict_agg(colunas_agg, 'sum', len(colunas_agg))

        grp_cum = base_cum.groupby(indice_agg).agg(dict_agg)
        grp_nao_cum = base_nao_cum.groupby(indice_agg).agg(dict_agg)


        somatorio_cum = grp_cum[colunas_somadas].sum(axis=1)
        somatorio_nao_cum = grp_nao_cum[colunas_somadas].max(axis=1)

        frames = [somatorio_cum, somatorio_nao_cum]
        somatorio = pd.concat(frames)

        filtro = somatorio >= 0

    else: # Caso padrão, usar para quando não houver físico realizado ou pessoa remunerada nas colunas.

        dict_agg = get_dict_agg(colunas_agg, 'sum', len(colunas_agg))

        grp = base.groupby(indice_agg).agg(dict_agg)

        #filtra para o grupo
        grp = filter_df_by_grupo(grupo, grp)


        somatorio = grp[colunas_somadas].sum(1)
        filtro = somatorio >= 0



    if filtro.all():
        print('\nRESULT: Sucesso.')
    else:
        print('\nRESULT: Falha')
        divergencias = grp[filtro == False]
        nome_arquivo = 'Cat 7 - ' + str(colunas_somadas[0][0:-4])
        diretorio = 'Divergencias/'
        grava_csv( nome_arquivo  , divergencias )




        
        
        
        
#__________________________________________________________________________________________________________________________________________

    
    
def grava_csv(diretorio, nome_arquivo, dataframe):
    
    dataframe.to_csv(diretorio + nome_arquivo+'.csv', sep=";", decimal=',', encoding='latin-1')

    print('\nO arquivo \"' +diretorio + nome_arquivo+ '.csv\" contém as divergências encontradas')

                  
                  
def verifica_bimestre(mes_final, bimestre_alvo):
    
    if ceil(mes_final/2) == bimestre_alvo:
        return True
    else:
        return False

    
def quebra_lista(lista,partes):
    return [lista[i::partes] for i in range(partes)]    
    

#__________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________
