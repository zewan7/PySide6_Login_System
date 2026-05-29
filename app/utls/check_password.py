

def validate_password(password):
    # 规则列表
    rules = [
        ('长度至少为8个字符', lambda p: len(p) >= 8),
        # ('包含至少一个大写字母', lambda p: any(c.isupper() for c in p)),
        # ('包含至少一个小写字母', lambda p: any(c.islower() for c in p)),
        ('包含至少一个字母', lambda p: any(c.isalpha() for c in p)),
        ('包含至少一个数字', lambda p: any(c.isdigit() for c in p)),
        # ('包含至少一个特殊字符', lambda p: any(not c.isalnum() and not c.isspace() for c in p)),
    ]

    failed_rules = []
    # 检查密码是否满足所有规则
    for rule_name, check in rules:
        if not check(password):
            failed_rules.append(rule_name)
            
    if failed_rules:
        return False, "密码要求：至少8个字符，且必须同时包含字母和数字"

    # 所有规则都通过
    return True, "密码有效"

