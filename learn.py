from manimlib import *


section1 = "类 的基本知识"
"""
## 类 的基本知识
哦对了，其实float list这些也是类呢。
"""

class Person:
    zhexiakandongle = "人类" # 这里面是“类属性”
    def __init__(self, name, age): # __init__()方法是类的构造方法，在创建类的实例时自动调用
        # self 参数指的是实例本身
        self.name = name # 这里面就是“实例属性”
        self.age = age

    def meow(self): 
        # 既然 self 参数指的是实例本身，绑定到实例，所以这里的方法是【实例方法】
        """
        让一个人喵喵叫，会print
        """
        print(f"{self.name} says meow. 可爱捏")

    @classmethod 
    # 这里是一个【修饰器】，把定义出来的方法绑定到类而不是实例
    # 但是实例也可以访问类方法
    # 
    def set_species(cls, species): # cls 就是类（class）
        cls.species = species # 咦，这都有类属性哦，吼吼吼吼

    # 其他的以后再学吧……


person1 = Person("Alice", 30)
print(person1.age) # 30
print(person1.zhexiakandongle) # "人类"
person1.meow()
Person.set_species("animal")
print(person1.species)

#################################### 分割线 #######################################################
section2 = "学manim"
"""
## 学manim
"""

class InteractiveDevelopment(Scene):
    def construct(self):
        # 实例化与设置一个圆
        circle = Circle() 
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)

        # 普普通通的方形
        square = Square()

        self.play(ShowCreation(square)) # ShowCreation 是一个动画类
        # self.wait()

        self.embed()  # 打开 iPython 终端，进入交互式开发模式。这个选项必带啊我看

        # 尝试拷贝粘贴下面这些行到交互终端中
        self.play(ReplacementTransform(square, circle))
        self.wait()
        self.play(circle.animate.stretch(4, 0))
        self.play(Rotate(circle, 90 * DEGREES))
        self.play(circle.animate.shift(2 * RIGHT).scale(0.25))

        text = Text("""
            In general, using the interactive shell
            is very helpful when developing new scenes
        """)
        self.play(Write(text))

        # 在交互终端中，你可以使用play, add, remove, clear, wait, save_state
        # 和restore来代替self.play, self.add, self.remove……

        # 这时如果要使用鼠标键盘来与窗口互动，需要输入执行touch()
        # 然后你就可以滚动窗口，或者在按住z时滚动来缩放
        # 按住d时移动鼠标来更改相机视角，按r重置相机位置
        # 按q退出和窗口的交互来继续输入其他代码

        # 特别的，你可以自定一个场景来和鼠标和键盘互动
        always(circle.move_to, self.mouse_point)

class AnimatingMethod(Scene): # 动画调用
    def construct(self): # construct 是 AnimatingMethod(Scene) 的一个方法。
        grid = Tex(r"\pi").get_grid(10, 10, height=4) # 这里有一“网”的\pi. height 指的是 Mobject 的尺寸
        self.add(grid)

        self.wait()
        
        self.play(grid.animate.shift(LEFT)) 
        self.wait()
        # ShowCreation、ReplacementTransform 这些都是 Animation 的后裔
        # 但 shift、stretch 这些都是 Mobject 类的实例方法。

        # x.animate.x
            # animate 是 Mobject 类的一个property属性，返回
            # 一个 _AnimationBuilder 代理对象，它会
            # 记录对 Mobject 调用的每一个变换方法，
            # 但不会立即执行，可以传入 play 方法来把他们
            # 变成【动画】而非【瞬移】
            # 当然，【瞬移】也可以设置 play 里 run_time=0

        # 瞬移
        grid.shift(LEFT)
        self.wait()
        grid.shift(RIGHT)

        self.wait()
        self.play(grid.animate.set_color(YELLOW)) # 色
        self.wait()
        self.play(grid.animate.set_submobject_colors_by_gradient(BLUE, GREEN)) # 渐变色
        self.wait()
        self.play(grid.animate.set_height(TAU - MED_SMALL_BUFF))
        self.wait()

        self.play(grid.animate.apply_complex_function(np.exp), run_time=5)
        self.wait()