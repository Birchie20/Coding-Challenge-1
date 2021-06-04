from abc import ABC, abstractmethod
import pandas as pd
import datetime


class IGenerateData(ABC):

    @abstractmethod
    def produce_report_data(self, report, date):
        """Interface Method"""


class GenerateDataClient1Report1(IGenerateData):
    """Used to generate the data needed for the report"""

    def __init__(self):
        self._report_date = None
        self._data = None

    def produce_report_data(self, report_date, data):
        """Used to produce the data required for this particular report"""
        self._data = data

        if isinstance(report_date, datetime.datetime):
            self._report_date = report_date.date()
        else:
            self._report_date = report_date

        report_df = self.create_df_for_report()

        results_dict = {'commissions': {}}

        results_dict['items'] = self.get_total_items(report_df)
        results_dict['customers'] = self.get_total_customers(report_df)
        results_dict['total_discount_amount'] = round(self.get_total_discount(report_df), 2)
        results_dict['discount_rate_avg'] = round(self.get_average_discount(report_df), 2)
        results_dict['order_total_avg'] = round(self.get_average_order(report_df), 2)
        results_dict['commissions']['total'] = round(self.get_total_commission(report_df), 2)
        results_dict['commissions']['order_average'] = round(self.get_average_commission_per_order(report_df), 2)
        results_dict['commissions']['promotions'] = self.get_total_commission_per_promo(report_df, data.promotions)

        return results_dict

    def create_df_for_report(self):
        """merges/generates all the data together to create a df which contains all the required data"""

        orders_at_date_df = self._data.orders.loc[self._data.orders.created_at.dt.date == self._report_date, :]
        commissions_at_date_df = self._data.commissions.loc[self._data.commissions.date.dt.date == self._report_date, :]
        promotions_on_day_df = self._data.product_promotions.loc[self._data.product_promotions.date.dt.date == self._report_date, :]
        
        report_df = pd.merge(left = orders_at_date_df, right = self._data.order_lines, how = 'left', left_on = 'id', right_on = 'order_id')
        report_df = pd.merge(left = report_df, right = commissions_at_date_df, how = 'left', on = 'vendor_id')
        
        Number_of_nulls = report_df.isna().sum().sum()
        if Number_of_nulls > 0:
            raise ValueError(f"Data sets do not correspond correctly - please check the following files and fields to ensure they tally:\n\norders\n\tid\norderlines\n\torder_id\n\tvendor_id\ncommissions\n\tvendor_id")
        
        report_df = pd.merge(left = report_df, right = promotions_on_day_df, how = 'left', on = 'product_id')

        report_df['commission'] = report_df['discounted_amount'] * report_df['rate']

        return report_df

    def get_total_items(self, report_df):
        """Used to return the number of orders placed in df"""

        return report_df.loc[:, 'quantity'].sum()

    def get_total_customers(self, report_df):
        """Used to get total customers in df"""

        return len(report_df.loc[:, 'customer_id'].unique())

    def get_total_discount(self, report_df):
        """Used to get the total discount in df"""

        return report_df.loc[:, 'full_price_amount'].sum() - report_df.loc[:, 'discounted_amount'].sum()

    def get_average_discount(self, report_df):
        """Used to get the average discount rate applied in df"""

        return report_df.loc[:, 'discount_rate'].sum() / report_df.loc[:, 'discount_rate'].count()

    def get_average_order(self, report_df):
        """Used to get the average order value in df"""

        grouped_order_totals = report_df.loc[:, ('order_id','total_amount')].groupby('order_id').sum()

        return grouped_order_totals['total_amount'].sum() / grouped_order_totals['total_amount'].count()

    def get_total_commission(self, report_df):
        """Used to get the total commission in df"""

        return report_df.loc[:, 'commission'].sum()

    def get_average_commission_per_order(self, report_df):
        """Used to get the average commission per order in df"""

        total_commission_per_order = report_df.loc[:, ('id', 'commission')].groupby('id').sum()

        return float(total_commission_per_order.sum() / total_commission_per_order.count())

    def get_total_commission_per_promo(self, report_df, promotions_df):
        """Used to get the average commission per promotion in df"""

        commission_by_promotion = report_df.loc[:, ('promotion_id', 'commission')].groupby('promotion_id').sum()

        commissions_template = promotions_df

        df_commmissions_by_promo = pd.merge(left = commissions_template, right = commission_by_promotion, how = 'left', left_on = 'id', right_on = 'promotion_id')
        df_commmissions_by_promo = df_commmissions_by_promo.loc[:, ('id', 'commission')]
        df_commmissions_by_promo = df_commmissions_by_promo.fillna(0)
        df_commmissions_by_promo = df_commmissions_by_promo.astype({'id': str})
        df_commmissions_by_promo['commission'] = df_commmissions_by_promo['commission'].apply(lambda x : round(x,2))

        return df_commmissions_by_promo.set_index('id').to_dict()['commission']

class GenerateReportFactory(object):
    """Used to generate the appropriate class to generate the report requested"""

    def __init__(self, client, report):
        self._client = client
        self._report = report


    def create_report_generator_obj(self):
        """Used to actually create the appropriate obj given the client and report"""

        if self._client == 'Client1':
            if self._report == 'report_1':
                return GenerateDataClient1Report1()
            else:
                raise ValueError(f"Report type requested not available for this client")
        else:
            raise ValueError(f"Client not recognised on system - please check with your provider")