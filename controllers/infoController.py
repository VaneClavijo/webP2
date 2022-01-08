from App import App
from flask import render_template, session, request, redirect, url_for
from App import db
from models.models import*
from flask import flash
from datetime import date


@App.route('/contract_report', methods=['POST', 'GET'])
def contract_report():
    contracts=Contract.query.filter(Contract.contract_state=='VIGENTE').all()
    gestores=Manager.query.filter().all()
    for c in contracts:
        if c.contract_end<date.today() and c.contract_state=='VIGENTE':
            db.session.query(Contract).filter(Contract.contract_id==c.contract_id).update(dict(contract_state='VENCIDO'))
            db.session.commit()
    if session["type"] in ['A']:
        contracts=Contract.query.filter(Contract.manager_id==None,Contract.contract_state!='CERRADO').all()
        if request.method == 'POST':
            id=request.form['idin']
            db.session.query(Contract).filter(Contract.contract_id==id).update(dict(contract_state='CERRADO',contract_close=date.today()))
            db.session.commit()
            flash('Contrato Cerrado con éxito')
            return redirect(url_for('contract_report'))
    elif session["type"] in ['M']:
        mng=Manager.query.filter(Manager.manager_ci==session["id"]).first()
        contracts=Contract.query.filter(Contract.manager_id==mng.manager_id,Contract.contract_state!='CERRADO').all()
        if request.method == 'POST':
            id=request.form['idin']
            db.session.query(Contract).filter(Contract.contract_id==id).update(dict(contract_state='CERRADO',contract_close=date.today()))
            db.session.commit()
            flash('Contrato Cerrado con éxito')
            return redirect(url_for('contract_report'))
    return render_template('contractReport.html', contracts = contracts,gestores=gestores)

@App.route('/level_contract_report', methods=['POST', 'GET'])
def level_contract_report():
    contract=Contract.query.filter(Contract.manager_id!=None,Contract.contract_state!='CERRADO',Contract.contract_instate=='INGRESO').all()
    contractg=[]
    for c in contract:
        n=Level.query.filter(Level.contract_id==c.contract_id).all()
        mng=Manager.query.filter(Manager.manager_id==c.manager_id).first()
        contractg.append((c.contract_id,
                        c.contract_provider,
                        c.contract_name,
                        mng.manager_name,
                        len(n),
                        n))
    if request.method == 'POST':
        id=request.form['idin']
        db.session.query(Contract).filter(Contract.contract_id==id).update(dict(contract_instate='CALIFICAR'))
        db.session.commit()
        flash('Contrato Cerrado con éxito')
        return redirect(url_for('level_contract_report'))

    return render_template('addLevel.html',contractg=contractg)

@App.route('/close_contract_report', methods=['POST', 'GET'])
def close_contract_report():
    contracts=Contract.query.filter(Contract.contract_state=='CERRADO').all()
    #db.session.query(User).join( Document ).join( DocumentsPermissions ).filter( User.email == "user@email.com" ).all()
    return render_template('closeContractReport.html', contracts = contracts)



