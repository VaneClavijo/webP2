from App import App
from flask import render_template, session, request, redirect, url_for
from App import db
from models.models import*
import datetime
from werkzeug.security import generate_password_hash
from sqlalchemy import or_
from flask import flash
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import time


send_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


@App.route('/add_manager', methods=['POST', 'GET'])
def add_manager():
    areas=Area.query.filter().all()

    if request.method=='POST':
        manager_ci=request.form['manager_ci']
        manager_name=request.form['manager_name']
        manager_email=request.form['manager_email']
        manager_phone=request.form['manager_phone']
        area_id=request.form['manager_area']
        manager_area=Area.query.filter_by(area_id=area_id).first()
        registro=Manager(manager_ci=manager_ci,
                        manager_name=manager_name,
                        manager_email=manager_email,
                        manager_phone=manager_phone,
                        area_id=area_id,
                        manager_area=manager_area)
        password=generate_password_hash(manager_ci, method='sha256')
        registroU=User(user_ci=manager_ci,
                        user_type='M',
                        user_name=manager_name,
                        password_hash=password)
        try:
            db.session.add(registro)
            db.session.commit()
            db.session.add(registroU)
            db.session.commit()
            flash('Registro guardado con éxito!')
        except IntegrityError:
            db.session.rollback()
            # Don't stop the stream, just ignore the duplicate.
            flash('Registro No Guardado')
    return render_template('addManager.html',areas=areas)


@App.route('/assing_manager', methods=['POST', 'GET'])
def assing_manager():
    if request.method=='POST':
        contract_id=request.form['idin']
        manager_id=request.form['manager_id']

        Contract.query.filter_by(contract_id=contract_id).update(dict(manager_id=manager_id,
                                                                    contract_instate='INGRESO'))
        db.session.commit()
        flash('Registro guardado con éxito!')

    return redirect(url_for('contract_report'))

@App.route('/add_level', methods=['POST', 'GET'])
def add_level():
    if request.method=='POST':
        level_name=request.form['level_name']
        level_goal=request.form['level_goal']
        contract_id=request.form['contract_id']
        contract=Contract.query.filter_by(contract_id=contract_id).first()
        registro=Level(level_name=level_name,
                        level_goal=level_goal,
                        contract_id=contract_id,
                        contract=contract)
        try:
            db.session.add(registro)
            db.session.commit()
            flash('Registro guardado con éxito!')
        except IntegrityError:
            db.session.rollback()
            # Don't stop the stream, just ignore the duplicate.
            flash('Registro No Guardado')
    return redirect(url_for('level_contract_report'))

@App.route('/add_score', methods=['POST', 'GET'])
def add_score():
    contractsf=db.session.query(Contract.contract_id,
                            Contract.contract_provider,
                            Contract.contract_name,
                            Contract.manager_id).filter().all()
    manager=db.session.query(Manager.manager_id).filter(Manager.manager_ci==session['id']).first()
    contracts=dict()
    for c in contractsf:
        if c.manager_id in manager:
            contracts[c.contract_id]=(c.contract_provider,c.contract_name)
    levels=db.session.query(Level).filter().all()
    ls=[]
    for l in levels:
        if l.contract_id in contracts.keys() :
            ls.append(l)
    cons=[]
    print(ls)
    for cs in ls:
        scores=db.session.query(Score).filter(Score.level_id==cs.level_id,
                                             Score.score_year==int(datetime.now().year),
                                             Score.score_month==int(datetime.now().month)).all()
        if not scores:
            cons.append((contracts[cs.contract_id],cs))
        print(scores)
        print(cons)
    print(contracts)
    if request.method=='POST':
        level_id=request.form['idin']
        score_value=request.form['score_value']
        score_month=int(datetime.now().month)
        score_year=int(datetime.now().year)
        registro=Score(score_value=score_value,
                        score_month=score_month,
                        level_id=level_id,
                        score_year=score_year)
        try:
            print(db.session.add(registro))
            db.session.commit()
            flash('Registro guardado con éxito!')
        except IntegrityError:
            db.session.rollback()
            # Don't stop the stream, just ignore the duplicate.
            flash('Registro No Guardado')
        return redirect(url_for('add_score'))
    return render_template('addScore.html',contracts=contracts,cons=cons)
