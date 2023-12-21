import re
class User:
    user_id = 0

    def __init__(self, name, sex, phone, qq, email):
        User.user_id += 1
        self.user_id = User.user_id
        self.name = name
        self.sex = sex
        self.phone = phone
        self.qq = qq
        self.email = email


class UserManager:
    def __init__(self):
        self.users = []


    def add_user(self, name, sex, phone, qq, email):
        while not self.is_valid_sex(sex):
            print("性别输入错误，请输入男或女")
            sex = input("请重新输入用户性别：")
        while not self.is_valid_phone(phone):
            print("手机号格式不正确")
            phone = input("请重新输入用户手机号：")

        user = User(name, sex, phone, qq, email)
        self.users.append(user)
        return user.user_id

    # 判断手机号格式是否正确
    def is_valid_phone(self, phone):
        # 正则表达式
        pattern = r'^1[0-9]{10}$'
        return re.match(pattern, phone) is not None

    # 判断性别格式是否正确
    def is_valid_sex(self, sex):
        return sex.lower() in ['男', '女']

    def display_all_users(self):
        if not self.users:
            print("用户列表为空")
            return
        print(f"用户ID\t姓名\t性别\t手机号\t\tQQ号码\t\t邮箱")
        for user in self.users:
            print("-------------------------------------------------")
            print(f"{user.user_id}\t{user.name}\t\t{user.sex}\t\t{user.phone}\t{user.qq}\t\t{user.email}")

    def display_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                print(f"用户ID 姓名\t性别\t\t手机号\t\tQQ号码\t\t邮箱")
                print("-------------------------------------------------")
                print(f"{user.user_id}\t{user.name}\t\t{user.sex}\t\t{user.phone}\t{user.qq}\t\t{user.email}")
                return
        print("找不到该用户")

    def update_phone(self, user_id, new_phone):
        for user in self.users:
            if user.user_id == user_id:
                while not self.is_valid_phone(new_phone):
                    print("手机号格式不正确")
                    new_phone = input("请重新输入用户手机号：")
                user.phone = new_phone
                print("手机号已更新")
                return
        print("找不到该用户")

    def run(self):
        while True:
            print("\n================ 用户管理系统 ================")
            print("1. 新增用户")
            print("2. 显示全部用户信息")
            print("3. 显示某位用户信息")
            print("4. 更新某位用户手机号信息")
            print("5. 退出系统")

            choice = input("请输入您选择的操作（输入数字）：")

            if choice == "1":
                name = input("请输入用户姓名：")
                sex = input("请输入用户性别（男/女）：")
                phone = input("请输入用户手机号：")
                qq = input("请输入用户QQ号码：")
                email = input("请输入用户邮箱：")
                user_id = self.add_user(name, sex, phone, qq, email)
                print(f"新增用户成功，用户ID: {user_id}")

            elif choice == "2":
                self.display_all_users()

            elif choice == "3":
                user_id = int(input("请输入要查询的用户ID："))
                self.display_user(user_id)

            elif choice == "4":
                user_id = int(input("请输入要更新手机号的用户ID："))
                new_phone = input("请输入新的手机号：")
                self.update_phone(user_id, new_phone)

            elif choice == "5":
                print("感谢使用用户管理系统，再见！")
                break

            else:
                print("无效的选择，请重新输入")


if __name__ == "__main__":
    UserManager().run()