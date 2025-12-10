import dns.resolver
import concurrent.futures


def check_domain(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX', raise_on_no_answer=False)
        if answers:
            return domain, "домен валиден"
        else:
            return domain, "MX-записи отсутствуют или некорректны"
    except dns.resolver.NoAnswer:
        return domain, "MX-записи отсутствуют или некорректны"
    except dns.resolver.NXDOMAIN:
        return domain, "домен отсутствует"
    except Exception as e:
        return domain, f"Ошибка: {e}"


def main():
    # Пример списка email-адресов
    emails = [
        "test@gmail.com",
        "example@nonexistentdomain.xyz",
        "user@mail.ru",
        "invalidemail@domain.withoutmx"
    ]

    # Парсим домены
    domains = set()
    email_domain_map = {}
    for email in emails:
        try:
            local_part, domain = email.strip().split('@')
            domains.add(domain)
            email_domain_map[email] = domain
        except ValueError:
            print(f"{email}: некорректный email")

    # Проверка доменов параллельно
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_domain, d) for d in domains]
        results = {}
        for future in concurrent.futures.as_completed(futures):
            try:
                domain, status = future.result()
                results[domain] = status
            except Exception as e:
                # Обработка ошибок:
                results[domain] = f"Ошибка при проверке: {e}"

    # Вывод результатов для каждого email
    for email in emails:
        domain = email_domain_map.get(email)
        if domain:
            print(f"{email}: {results.get(domain, 'не проверено')}")
        else:
            print(f"{email}: некорректный email")


if __name__ == "__main__":
    main()
