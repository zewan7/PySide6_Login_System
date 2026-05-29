from email_validator import validate_email, EmailNotValidError


def validate_email_with_lib(email):
    """
    邮箱验证
    """
    try:
        # 禁用 check_deliverability 以防止 Windows 下 dns 解析器因注册表编码问题报错 (embedded null character)
        validate_email(email, check_deliverability=False)
        return True
    except EmailNotValidError:
        return False
