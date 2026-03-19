from flask import Blueprint, render_template, request, redirect, url_for, flash
import datetime
import psycopg2
from db import conn
user = 3

route_bp = Blueprint('route', __name__)

@route_bp.route("/route")
def route():
    view_type = request.args.get('type')
    if view_type == "manage":
        curr = conn.cursor()
        curr.execute("SELECT id, route_code, route_name, active FROM blg_routemaster")
        data = curr.fetchall()
        curr.close()
        return render_template("route.html",data=data,type=view_type)
    elif view_type == "add":
        return render_template("route.html",type=view_type)
    else:
        return render_template("route.html",type=view_type)


@route_bp.route("/route/<int:id>", methods=['POST','GET'])
def routeEdit(id):
    curr = conn.cursor()
    if request.method == "GET":
        sql = f"""
SELECT
    created_date, 
    created_by, 
    company_id, 
    route_code, 
    route_name, 
    last_sup_no, 
    route_order, 
    route_device_no, 
    gps_location, 
    status, 
    active, 
    route_manager_id, 
    consolidation_id, 
    transportid, 
    category_01, 
    category_02, 
    category_03, 
    category_04, 
    category_05 FROM blg_routemaster WHERE id = %s
"""
        curr.execute(sql,(id,))
        data = curr.fetchone()
        data = ["" if x is None else x for x in data]
        curr.close()
        return render_template("routeedit.html",s=data,id=id)
    

    if request.method == 'POST':
        sql = """
UPDATE blg_routemaster SET 
    updated_by = %(UpdatedBy)s,
    updated_date = %(UpdatedDate)s,
    company_id = %(CompanyId)s,
    route_code = %(RouteCode)s,
    route_name = %(RouteName)s,
    last_sup_no = %(LastSupNo)s,
    route_order = %(RouteOrder)s,
    route_device_no = %(RouteDeviceNo)s,
    gps_location = %(GPSLocation)s,
    status = %(Status)s,
    active = %(active)s,
    route_manager_id = %(RouteManagerId)s,
    consolidation_id = %(ConsolidationId)s,
    transportid = %(TransportId)s,
    category_01 = %(category_01)s,
    category_02 = %(category_02)s,
    category_03 = %(category_03)s,
    category_04 = %(category_04)s,
    category_05 = %(category_05)s
WHERE id = %(id)s;"""

        data = request.form.to_dict()

        for x in data.keys():
            if data[x].strip() == "":
                data[x] = None

        data["UpdatedBy"] = user
        data["UpdatedDate"] = datetime.date.today()
        data["active"] = bool(request.form.get('active'))
        data["id"] = id

        try:
            
            curr.execute(sql, data)
            conn.commit()
            flash("Route updated successfully!", "success")

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            flash(f"Error updating the route", "danger")
        
        finally:
            curr.close()

            return redirect(url_for("route.route",type="manage"))


@route_bp.route("/route/add", methods=['POST'])
def routeAdd():
    curr = conn.cursor()
    sql = f"""INSERT INTO blg_routemaster (
    created_date, 
    created_by, 
    updated_by, 
    updated_date, 
    company_id, 
    route_code, 
    route_name, 
    last_sup_no, 
    route_order, 
    route_device_no, 
    gps_location, 
    status, 
    active, 
    route_manager_id, 
    consolidation_id, 
    transportid, 
    category_01, 
    category_02, 
    category_03, 
    category_04, 
    category_05
) 
VALUES (
    %(CreatedDate)s,      
    %(CreatedBy)s,              
    %(UpdatedBy)s,               
    %(UpdatedDate)s,    
    %(CompanyId)s,               
    %(RouteCode)s,              
    %(RouteName)s,              
    %(LastSupNo)s,               
    %(RouteOrder)s,               
    %(RouteDeviceNo)s,               
    %(GPSLocation)s,               
    %(Status)s,               
    %(active)s,              
    %(RouteManagerId)s,               
    %(ConsolidationId)s,               
    %(TransportId)s,               
    %(category_01)s,               
    %(category_02)s,               
    %(category_03)s,               
    %(category_04)s,               
    %(category_05)s                
);"""
    data = request.form.to_dict()

    for x in data.keys():
        if data[x].strip() == "":
            data[x] = None

    data["CreatedDate"] = datetime.date.today()
    data["CreatedBy"] = user
    data["UpdatedBy"] = user
    data["UpdatedDate"] = datetime.date.today()
    data["active"] = bool(request.form.get('active'))

    try:
        
        curr.execute(sql, data)
        conn.commit()
        flash("Route added successfully!", "success")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        flash(f"Error adding the route: {error}", "danger")

    finally:
        curr.close()
        
        return redirect(url_for("route.route" ,type=""))