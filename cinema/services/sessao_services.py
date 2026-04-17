from cinema.data import loading_db
from datetime import datetime, date

def get_section_by_date_hour(filme):
    sessoes = loading_db.load_sections(filme.id)
    datas = set()
    datas_formatadas = []
    horarios = set()
    datas_dict = {}

    if sessoes:
        for sessao in sessoes:
            data_hora = sessao["data_hora"]
            data, hora = str(data_hora).replace(' ', '_').split('_')


            if data not in datas_dict:
                datas_dict[data] = []

            datas_dict[data].append(hora)
            
            datas.add(data)
            horarios.add(hora)
    
    datas_ordenadas = sorted(
        datas_dict.keys(),
        key=lambda d: datetime.strptime(d, '%Y-%m-%d'))
 

    for data in datas_ordenadas:
        data_obj = datetime.strptime(data, '%Y-%m-%d')
        hoje = date.today()

        data_formatada = data_obj.strftime('%d/%m')
        dia_semana = data_obj.strftime('%A')

        dias = {
            "Monday": "Segunda",
            "Tuesday": "Terça",
            "Wednesday": "Quarta",
            "Thursday": "Quinta",
            "Friday": "Sexta",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }

        dia_br = dias[dia_semana]        

        if data_obj.date() == hoje:
            texto = f"Hoje ({data_formatada} - {dia_br})"
        else:
            texto = f"{data_formatada} ({dia_br})"

        datas_formatadas.append({
            "data": data,
            "horarios": sorted(datas_dict[data]),
            "label": texto
        })

    return datas_formatadas

def get_section(filme, data_hora):
    sessoes = loading_db.load_sections(filme.id)
    # print(sessoes)
    data_hora = datetime.strptime(data_hora, "%Y-%m-%d_%H:%M:%S")
    if sessoes:
        for sessao in sessoes:
            if sessao.get('data_hora') == data_hora:
                return sessao
            
    return None