from django.shortcuts import render, redirect
from .forms import EmployeeForm
from .models import Employee
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import openpyxl
from reportlab.pdfgen import canvas
from django.core.paginator import Paginator
from django.contrib.auth import logout

def logout_user(request):
    logout(request)
    return redirect("/login/")


def home(request):
    search = request.GET.get("search")

    total_employees = Employee.objects.count()
    cs_count = Employee.objects.filter(department__iexact='CS').count()
    it_count = Employee.objects.filter(department__iexact='IT').count()
    hr_count = Employee.objects.filter(department__iexact='HR').count()

    if search:
        employees = Employee.objects.filter(name__icontains=search)
    else:
        employees = Employee.objects.all()

        paginator = Paginator(employees, 10)
        page_number = request.GET.get('page')
        employees = paginator.get_page(page_number)

    return render(request, "home.html", {
        "employees": employees,
        "search": search,
        "total_employees": total_employees,
         "cs_count": cs_count,
         "it_count": it_count,
         "hr_count": hr_count,
    })


def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = EmployeeForm()


    return render(request, "add_employee.html", {"form": form})
def edit_employee(request, id):
    employee = Employee.objects.get(id=id)

    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = EmployeeForm(instance=employee)

    return render(request, "add_employee.html", {"form": form})


def delete_employee(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return redirect("/")

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html", {
                "error": "Invalid Username or Password"
            })

    return render(request, "login.html")

def export_excel(request):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Employees"

    worksheet.append([
        "ID",
        "Name",
        "Email",
        "Phone",
        "Department"
    ])

    employees = Employee.objects.all()

    for employee in employees:
        worksheet.append([
            employee.id,
            employee.name,
            employee.email,
            employee.phone,
            employee.department,
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = 'attachment; filename="employees.xlsx"'

    workbook.save(response)

    return response

def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="employees.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(180, 800, "Employee Report")

    p.setFont("Helvetica", 12)

    y = 760

    employees = Employee.objects.all()

    for employee in employees:
        line = (
            f"ID: {employee.id} | "
            f"Name: {employee.name} | "
            f"Email: {employee.email} | "
            f"Dept: {employee.department}"
        )

        p.drawString(40, y, line)

        y -= 25

        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 12)
            y = 800

    p.save()

    return response
