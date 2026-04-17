from manimlib import *

# 想要实现幻灯片化，可以用input。或者键盘监听。


class SquareToCircle(Scene):    #Scene的子类
    def construct(self):
        circle = Circle() # mobject 的实例化

        # mobject 实例的设置是通过 method
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        
        square = Square()



        # 这些动画其实都是动画类，
        # 如：
        # self.play(Animation(动画对象))
        # self.wait()

        self.play(ShowCreation(square)) 
        self.wait()
        self.play(ReplacementTransform(square, circle)) # ReplacementTransform “圆变方”的核心
        self.wait()

        # 在播完后可交互地一句一句地播放。
        # play(Animation) 即可，不必写self.play(Animation)
        self.embed()

class AddRemoveShowCreation(Scene):
    def construct(self):
        # 各个Mobject的实例化（创建）
        circle = Circle() # 创建一个Circle的实例：circle

        #动画
        self.add(circle)
        self.wait()
        self.remove(circle)
        self.wait()
        self.play(ShowCreation(circle)) #ShowCreation是“画”出来的。

class ShiftMethod(Scene):
    def construct(self):
        #实例化
        circle = Circle()
        triagle = Triangle()
        square = Square()

        #实例的相关设置
        circle.shift(LEFT)
        triagle.shift(UP)
        square.shift(RIGHT)
        circle.set_fill(BLUE, opacity=1) # opacity是不透明度（实心度）
        circle.set_stroke(BLUE_E)

        #add
        self.add(circle, triagle, square)
        self.wait()
        self.remove(circle)
        self.wait()
        self.play(ShowCreation(circle)) # play是画出来。


class AnimatingMethods(Scene):
    def construct(self):
        grid = Tex(r"\pi").get_grid(10, 10, height=4)
        self.add(grid)

        # You can animate the application of mobject methods with the
        # ".animate" syntax:
        self.play(grid.animate.shift(LEFT))

        # Alternatively, you can use the older syntax by passing the
        # method and then the arguments to the scene's "play" function:
        self.play(grid.shift, LEFT)

        # Both of those will interpolate between the mobject's initial
        # state and whatever happens when you apply that method.
        # For this example, calling grid.shift(LEFT) would shift the
        # grid one unit to the left, but both of the previous calls to
        # "self.play" animate that motion.

        # The same applies for any method, including those setting colors.
        self.play(grid.animate.set_color(YELLOW))
        self.wait()
        self.play(grid.animate.set_submobject_colors_by_gradient(BLUE, GREEN))
        self.wait()
        self.play(grid.animate.set_height(TAU - MED_SMALL_BUFF))
        self.wait()

        # The method Mobject.apply_complex_function lets you apply arbitrary
        # complex functions, treating the points defining the mobject as
        # complex numbers.
        self.play(grid.animate.apply_complex_function(np.exp), run_time=5)
        self.wait()

        # Even more generally, you could apply Mobject.apply_function,
        # which takes in functions form R^3 to R^3
        self.play(
            grid.animate.apply_function(
                lambda p: [
                    p[0] + 0.5 * math.sin(p[1]),
                    p[1] + 0.5 * math.sin(p[0]),
                    p[2]
                ]
            ),
            run_time=5,
        )
        self.wait()