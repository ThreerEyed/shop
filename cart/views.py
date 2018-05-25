from django.shortcuts import render, redirect

from cart.models import Goods


def index(request):
    """
    这是首页的视图
    :param request:
    :return:
    """
    goods_list = list(Goods.objects.all())
    return render(request, 'goods.html', {'goods_list': goods_list})


class CartItem(object):
    """
    这是购物车项
    """
    def __init__(self, goods, amount=1):
        self.goods = goods
        self.amount = amount

    @property
    def total(self):
        """
        小计: 计算所买商品的价格.
        :return:
        """
        return self.goods.price * self.amount


class ShoppingCart(object):
    """
    购物车
    """
    def __init__(self):
        # self.num = 0
        self.items = {}

    def add_item(self, item):
        """
        增加项:
        :return:
        """
        if item.goods.id in self.items:
            self.items[item.goods.id].amount += item.amount
        else:
            self.items[item.goods.id] = item

    def remove_item(self, id):
        if id in self.items:
            self.items.remove(id)

    def clear_all_items(self):
        self.items.clear()

    @property
    def cart_items(self):
        return self.items.values()

    @property
    def total(self):
        val = 0
        for item in self.items.values():
            val += item.total
        return val


def add_to_cart(request, id):
    """
    这是添加到购物车的视图
    :param request:
    :param no:
    :return:
    """
    goods = Goods.objects.get(pk=id)
    # 通过request对象的session属性可以获取到session
    # session相当于是服务器端用来保存用户数据的一个字典
    # session 利用了Cookie 保存sessionid 通过sessionid就可以获取用户会话(也就是用户数据)
    # 如果在浏览器中清楚了Cookie 那么也就清楚了sessionid
    # 再次访问服务器时服务器会重新分配新的sessionid 这也就意味着之前的用户数据无法再找回
    # 默认情况下 Django 的session 被设定为持久会话 而非浏览器续存期回话
    # 通过SESSION_EXPIRE_AT_BROWSER_CLOSE 和  SESSION_COOKIE_AGE 参数可以修改默认设置
    # django 中的session 是进行了持久化处理的因此需要设定session的序列化方式
    # 1.6版开始 Django 默认的session 序列化是JsonSerializer
    # 可以通过 SESSION_SERIALIZER 来设定其他的序列化器(例如PickleSerializer)
    # cart = request.session.get('cart', ShoppingCart())
    # if not cart:
    #     cart = ShoppingCart()
    #     request.session.set('cart',cart)
    # item = CartItem(cart.num, goods)
    # cart.add_item(item)
    # cart.num += 1
    # request.session['cart'] = cart
    # return redirect('/')
    cart = request.session.get('cart', ShoppingCart())
    cart.add_item(CartItem(goods))
    request.session['cart'] = cart
    return redirect('/')


# def show_cart(request):
#     """
#     这是展示购物车的视图
#     :param request:
#     :return:
#     """
#     cart = request.session.get('cart', None)
#     cart_items = cart.items.values() if cart else []
#     total = cart.total if cart else 0
#     return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})
def show_cart(request):
    cart = request.session.get('cart', None)
    return render(request, 'cart.html', {'cart': cart})


def clean_cart(request):
    cart = request.session.get('cart')
    cart = {}
    return render(request, 'cart.html', {'cart': cart})
