class yyy:
    def a(self, a):
        print(a)
        ad = self.b(a)
        print(ad)



    def b(self,num):
        num = num +1
        return num

if __name__ == "__main__":
    y = yyy()
    y.a(12)