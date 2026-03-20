from flask import Blueprint, render_template, request, redirect, url_for, flash
import psycopg2
from db import conn

supplier_bp = Blueprint('supplier', __name__)
user = 3

@supplier_bp.route("/supplier")
def supplier():
    view_type = request.args.get('type')
    if view_type == "manage":
        curr = conn.cursor()
        curr.execute("SELECT id, reg_no, reg_name, is_active FROM bl_sup_register")
        data = curr.fetchall()
        curr.close()
        return render_template("supp.html", supp=data, type=view_type)
    elif view_type == "add":
        curr = conn.cursor()
        curr.execute("SELECT id FROM blg_routemaster")
        data = curr.fetchall()
        curr.close()
        return render_template("supp.html", supp=data ,type=view_type)
    else:
        return render_template("supp.html", type=view_type)


@supplier_bp.route("/supplier/delete/<int:id>")
def delete(id):

    curr = conn.cursor()
    curr.execute("SELECT is_active FROM bl_sup_register WHERE id = %s",(id,))
    data = curr.fetchone()[0]

    if data == True:
        curr.execute("UPDATE bl_sup_register SET is_active = %s WHERE id = %s",(False,id))
        flash("Supplier is successfully Deleted", "success")
    else:
        flash("Supplier is already Deleted", "danger")
    curr.close()
    return redirect(url_for("supplier.supplier",type="manage"))


@supplier_bp.route("/supplier/edit/<int:id>", methods=['GET','POST'])
def supplierEdit(id):
    if request.method == "GET":
        curr = conn.cursor()
        sql = f"""
SELECT created_by, 
    updated_by, 
    company_id, 
    product_id, 
    reg_no, 
    route_id, 
    partner_id, 
    reg_name, 
    bank_id, 
    bank_account, 
    welfare_registered, 
    saving_scheme_registered, 
    saving_amount, 
    other_scheme_registered, 
    collector, 
    collector_no, 
    branch_id, 
    pay_mode, 
    cf_coins, 
    dob, 
    enrolled_date, 
    notes, 
    bssmsstatus, 
    transporttype, 
    acreage, 
    hectreage, 
    rood, 
    purch, 
    analysiscode01, 
    analysiscode02, 
    analysiscode03, 
    analysiscode04, 
    analysiscode05, 
    advance_status, 
    advance_pay_type, 
    manure_tr_type, 
    manure_tr_id, 
    nic_no, 
    transport_id, 
    bank_account_name, 
    is_active, 
    address_line01, 
    address_line02, 
    address_line03, 
    address_line04, 
    estate_name, 
    telephone, 
    transport_incentive, 
    member_fee, 
    other_fee,
    supplier
    FROM bl_sup_register WHERE id = %s
"""
        curr.execute(sql,(id,))
        a = curr.fetchone()
        a = ["" if x is None else x for x in a]
        curr.close()
        return render_template("suppedit.html",id=id,a=a)
    
    if request.method == "POST":
        curr = conn.cursor()
        sql =  """
UPDATE bl_sup_register SET
    updated_by=%(updated_by)s,
    company_id=%(company_id)s,
    product_id=%(product_id)s,
    reg_no=%(reg_no)s,
    route_id=%(route_id)s,
    partner_id=%(partner_id)s,
    reg_name=%(reg_name)s,
    bank_id=%(bank_id)s,
    bank_account=%(bank_account)s,
    welfare_registered=%(welfare_registered)s,
    saving_scheme_registered=%(saving_scheme_registered)s,
    saving_amount=%(saving_amount)s,
    other_scheme_registered=%(other_scheme_registered)s,
    collector=%(collector)s,
    collector_no=%(collector_no)s,
    branch_id=%(branch_id)s,
    pay_mode=%(pay_mode)s,
    cf_coins=%(cf_coins)s,
    dob=%(dob)s,
    enrolled_date=%(enrolled_date)s,
    notes=%(notes)s,
    bssmsstatus=%(bssmsstatus)s,
    transporttype=%(transporttype)s,
    acreage=%(acreage)s,
    hectreage=%(hectreage)s,
    rood=%(rood)s,
    purch=%(purch)s,
    analysiscode01=%(analysiscode01)s,
    analysiscode02=%(analysiscode02)s,
    analysiscode03=%(analysiscode03)s,
    analysiscode04=%(analysiscode04)s,
    analysiscode05=%(analysiscode05)s,
    advance_status=%(advance_status)s,
    advance_pay_type=%(advance_pay_type)s,
    manure_tr_type=%(manure_tr_type)s,
    manure_tr_id=%(manure_tr_id)s,
    nic_no=%(nic_no)s,
    transport_id=%(transport_id)s,
    bank_account_name=%(bank_account_name)s,
    is_active=%(is_active)s,
    address_line01=%(address_line01)s,
    address_line02=%(address_line02)s,
    address_line03=%(address_line03)s,
    address_line04=%(address_line04)s,
    estate_name=%(estate_name)s,
    telephone=%(telephone)s,
    transport_incentive=%(transport_incentive)s,
    member_fee=%(member_fee)s,
    other_fee=%(other_fee)s,
    supplier=%(supplier)s
WHERE id=%(id)s
"""
        data = request.form.to_dict()

        for x in data.keys():
            if data[x].strip() == "":
                data[x] = None
        
        curr.execute("SELECT supplier FROM bl_sup_register WHERE id=%s",(id,))
        exfile = curr.fetchone()

        file = request.files.get('supplier')
        if file and file.filename != '':
            data['supplier'] = psycopg2.Binary(file.read())
        else:
            data['supplier'] = exfile[0]

        data["updated_by"] = user
        data["welfare_registered"] = bool(request.form.get('welfare_registered'))
        data["advance_status"] = bool(request.form.get('advance_status'))
        data["is_active"] = bool(request.form.get('is_active'))
        data["saving_scheme_registered"] = bool(request.form.get('saving_scheme_registered'))
        data["other_scheme_registered"] = bool(request.form.get('other_scheme_registered'))
        data["collector"] = bool(request.form.get('collector'))
        data["id"] = id

        try:
            
            curr.execute(sql, data)
            conn.commit()
            flash("Supplier updated successfully!", "success")

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            flash(f"Error updated supplier: {str(error)}", "danger")
            conn.rollback()
        
        finally:
            curr.close()
            return redirect(url_for("supplier.supplier" ,type="manage"))


@supplier_bp.route("/supplier/add", methods=['POST'])
def supplierAdd():

    curr = conn.cursor()
    sql = f"""
INSERT INTO public.bl_sup_register (
    created_by, 
    updated_by, 
    company_id, 
    product_id, 
    reg_no, 
    route_id, 
    partner_id, 
    reg_name, 
    bank_id, 
    bank_account, 
    welfare_registered, 
    saving_scheme_registered, 
    saving_amount, 
    other_scheme_registered, 
    collector, 
    collector_no, 
    branch_id, 
    pay_mode, 
    cf_coins, 
    dob, 
    enrolled_date, 
    notes, 
    bssmsstatus, 
    transporttype, 
    acreage, 
    hectreage, 
    rood, 
    purch, 
    analysiscode01, 
    analysiscode02, 
    analysiscode03, 
    analysiscode04, 
    analysiscode05, 
    advance_status, 
    advance_pay_type, 
    manure_tr_type, 
    manure_tr_id, 
    nic_no, 
    transport_id, 
    bank_account_name, 
    is_active, 
    address_line01, 
    address_line02, 
    address_line03, 
    address_line04, 
    estate_name, 
    telephone, 
    transport_incentive, 
    member_fee, 
    other_fee,
    supplier
) 
VALUES (
    %(created_by)s,
    %(updated_by)s,
    %(company_id)s,
    %(product_id)s,
    %(reg_no)s, 
    %(route_id)s,
    %(partner_id)s,
    %(reg_name)s,
    %(bank_id)s,
    %(bank_account)s, 
    %(welfare_registered)s,
    %(saving_scheme_registered)s,
    %(saving_amount)s, 
    %(other_scheme_registered)s,
    %(collector)s,
    %(collector_no)s,
    %(branch_id)s, 
    %(pay_mode)s,
    %(cf_coins)s, 
    %(dob)s, 
    %(enrolled_date)s, 
    %(notes)s, 
    %(bssmsstatus)s, 
    %(transporttype)s, 
    %(acreage)s, 
    %(hectreage)s, 
    %(rood)s, 
    %(purch)s, 
    %(analysiscode01)s, 
    %(analysiscode02)s, 
    %(analysiscode03)s, 
    %(analysiscode04)s, 
    %(analysiscode05)s, 
    %(advance_status)s, 
    %(advance_pay_type)s, 
    %(manure_tr_type)s, 
    %(manure_tr_id)s, 
    %(nic_no)s, 
    %(transport_id)s, 
    %(bank_account_name)s, 
    %(is_active)s, 
    %(address_line01)s, 
    %(address_line02)s, 
    %(address_line03)s, 
    %(address_line04)s, 
    %(estate_name)s, 
    %(telephone)s, 
    %(transport_incentive)s, 
    %(member_fee)s, 
    %(other_fee)s,
    %(supplier)s
)
"""
    
    data = request.form.to_dict()

    for x in data.keys():
        if data[x].strip() == "":
            data[x] = None

    file = request.files.get('supplier')
    if file and file.filename != '':
        data['supplier'] = psycopg2.Binary(file.read())
    else:
        data['supplier'] = None

    data["created_by"] = user
    data["updated_by"] = user
    data["welfare_registered"] = bool(request.form.get('welfare_registered'))
    data["welfare_registered"] = bool(request.form.get('welfare_registered'))
    data["advance_status"] = bool(request.form.get('advance_status'))
    data["is_active"] = bool(request.form.get('is_active'))
    data["saving_scheme_registered"] = bool(request.form.get('saving_scheme_registered'))
    data["other_scheme_registered"] = bool(request.form.get('other_scheme_registered'))
    data["collector"] = bool(request.form.get('collector'))

    try:
        
        curr.execute(sql, data)
        conn.commit()
        flash("Supplier created successfully", "success")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        flash(f"Error registering supplier: {str(error)}", "danger")
        conn.rollback()
    
    finally:
        curr.close()
        return redirect(url_for("supplier.supplier" ,type=""))