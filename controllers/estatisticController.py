from sqlalchemy.sql.elements import Null
from App import App
from flask import render_template
from App import db
from models.models import*
import datetime
from datetime import datetime


@App.route('/statistics', methods=['POST', 'GET'])
def statistics():
    contracts=db.session.query(Contract.contract_id,
                                Contract.contract_provider,
                                Contract.contract_name).filter(Contract.contract_state!='CERRADO',
                                                                Contract.contract_instate=='CALIFICAR').all()
    cons=[]
    for cs in contracts:
        levels=db.session.query(Level.level_id,Level.level_goal).filter(Level.contract_id == cs.contract_id).all()
        if not levels:
            cons.append((cs,('NA','NA')))
        else:
            sa=[]
            sm=[]
            for l in levels:
                scores=db.session.query(Score.score_value).filter(Score.level_id == l.level_id).all()
                scoresM=db.session.query(Score.score_value).filter(Score.level_id == l.level_id,
                                                                    Score.score_month==int(datetime.now().month),
                                                                    Score.score_year==int(datetime.now().year)).first()
                suma=0
                cont=0
                for s in scores:
                    suma=suma+s[0]
                    cont=cont+1
                if cont != 0:
                    sa.append(round(((suma/(cont*l.level_goal))*100),2))
                    sm.append(round(((scoresM[0]/l.level_goal)*100),2))
            if len(sa)!=0 and len(sm)!=0:
                cons.append((cs,(sum(sa)/len(sa),sum(sm)/len(sm))))
            else:
                cons.append((cs,('NC','NC')))
    contador=0
    acumuladoM=0
    acumuladoA=0
    for s in cons:
        if s[1][0]!='NA' and s[1][1]!='NA'  and s[1][1]!='NC' and s[1][0]!='NC':
            contador=contador+1
            acumuladoM=acumuladoM+s[1][1]
            acumuladoA=acumuladoA+s[1][0]

    return render_template('statistics.html',
                            contracts=contracts,
                            cons=cons,
                            contador=round(((contador/len(contracts))*100),2),
                            acumuladoM=round((acumuladoM/contador),2),
                            acumuladoA=round((acumuladoA/contador),2))