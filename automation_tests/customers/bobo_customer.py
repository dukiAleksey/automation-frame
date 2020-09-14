from customers.customer import Customer


class AbcApiCustomerBobo(Customer):
    def __init__(self, logger):
        super().__init__('Bobo_customer', logger)
        self.bugs_dict = {}

    def get_abc_url(self):
        return f"https://{self.configurator.get_abc_bobo_url()}"

    def get_abc_dashboard_title(self, locale):
        dashboard_titles = {
            'en-US': 'MY ACCOUNT'
        }
        return dashboard_titles[locale]

    @staticmethod
    def get_abc_source():
        return None

    def test_case_file_name(self):
        return 'ABC_API_BOBO'
