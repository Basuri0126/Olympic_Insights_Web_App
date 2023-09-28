import numpy as np


def country_year_list(df):
    years = df.Year.unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df.region.dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years, country


def fetch_medal_tally(df, year, country):
    flag = 0
    medal_df = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal', 'region'])
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(year))]

    if flag == 1:
        tally = temp_df.groupby('Year').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Year',
                                                                                                         ascending=True).reset_index()
    else:
        tally = temp_df.groupby('region').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                        ascending=False).reset_index()
    tally['total'] = tally['Gold'] + tally['Silver'] + tally['Bronze']
    return tally


def participate_country_over_time(df):
    nations_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index()
    nations_over_time.rename(columns={'region': 'Edition', 'count': 'No. of Countries'}, inplace=True)
    return nations_over_time.sort_values('Year', ascending=True)


def number_events_over_time(df):
    events_over_time = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index()
    events_over_time.rename(columns={'count': 'No. of Events'}, inplace=True)
    return events_over_time.sort_values('Year', ascending=True)


def athlete_over_time(df):
    athletes = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index()
    athletes.rename(columns={'count': 'No. of Athletes'}, inplace=True)
    return athletes.sort_values('Year', ascending=True)


def most_successful(df, selected_sport):
    temp_df = df.dropna(subset=['Medal'])

    if selected_sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == selected_sport]

    x = temp_df['Name'].value_counts().reset_index().head(20).merge(df, right_on='Name', left_on='Name', how='left')[
        ['Name', 'count', 'Sport', 'region']].drop_duplicates()
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x


def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(12).merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'count', 'Sport']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
