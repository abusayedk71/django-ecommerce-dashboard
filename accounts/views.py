from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import * 
from .forms import *
from .filters import OrderFilter

# Create your views here.
def registraionPage(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            #messages.success(request,'Account was created for' + user)
            return redirect("login")
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request,'registration/register.html', context)


@login_required
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders,'customers':customers, 'total_orders':total_orders,'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/dashboard.html',context)

@login_required
def products(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'accounts/products.html',context)

@login_required
def createProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/products')
    context = {'form':form}
    return render(request,'accounts/products_form.html',context)

@login_required
def updateProduct(request,pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/products')
    context ={'product':product,'form':form}
    return render(request,'accounts/products_form.html',context)

@login_required
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('/products')
    context = {'product':product}
    return render(request,'accounts/delete_product.html',context)

@login_required
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()

    filters = OrderFilter(request.GET, queryset=orders)
    orders = filters.qs
    context = {'customer': customer,'orders': orders,'total_orders': total_orders,'filters':filters}
    return render(request,'accounts/customer.html', context)

@login_required
def createCustomer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    context = {'form':form}
    return render(request,'accounts/customer_form.html',context)

@login_required
def updateCustomer(request,pk):
    customers = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customers)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customers)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    context ={'customers':customers,'form':form}
    return render(request,'accounts/update_customer_form.html',context)

@login_required
def deleteCustomer(request, pk):
    customers = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customers.delete()
        return redirect('/dashboard')
    context = {'customers':customers}
    return render(request,'accounts/delete_customer.html',context)

@login_required
def createOrder(request, pk):
    OrderFormSet =inlineformset_factory(Customer, Order, fields=('product', 'status'),extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer':customers})
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/dashboard')
    context = {'formset': formset}
    return render(request,'accounts/place_order_form.html', context)

@login_required
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    context = {'formset':form}
    return render(request,'accounts/update_order_form.html',context)

@login_required
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/dashboard')
    context = {'order':order}
    return render(request,'accounts/delete.html',context)

    





