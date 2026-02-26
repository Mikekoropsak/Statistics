def create_table1(df, condition_column:str):    
    df_u = df[['ssid', condition_column, 'sex', 'race', 'age_group']].drop_duplicates()

    condition_totals = (
        df_u.groupby(condition_column)['ssid']
            .nunique()
            .to_dict()
    )

    def n_pct(x, total):
        n = x.nunique()
        pct = n / total * 100 if total else 0
        return f"{n:,} ({pct:.1f}%)"

    overall_total = df_u['ssid'].nunique()


    def n_pct_overall(x):
        n = x.nunique()
        pct = n / overall_total * 100 if overall_total else 0
        return f"{n:,} ({pct:.1f}%)"


    sex_table = (
        df_u.groupby([condition_column, 'sex'])['ssid']
            .apply(lambda x: n_pct(x, condition_totals[x.name[0]]))
            .reset_index(name='value')
            .pivot(index='sex', columns=condition_column, values='value')
    )

    sex_overall = (
        df_u.groupby('sex')['ssid']
            .apply(n_pct_overall)
    )

    sex_table['Overall'] = sex_overall


    race_table = (
        df_u.groupby([condition_column, 'race'])['ssid']
            .apply(lambda x: n_pct(x, condition_totals[x.name[0]]))
            .reset_index(name='value')
            .pivot(index='race', columns=condition_column, values='value')
    )

    race_overall = (
        df_u.groupby('race')['ssid']
            .apply(n_pct_overall)
    )

    race_table['Overall'] = race_overall


    age_table = (
        df_u.groupby([condition_column, 'age_group'])['ssid']
            .apply(lambda x: n_pct(x, condition_totals[x.name[0]]))
            .reset_index(name='value')
            .pivot(index='age_group', columns=condition_column, values='value')
    )

    age_overall = (
        df_u.groupby('age_group')['ssid']
            .apply(n_pct_overall)
    )

    age_table['Overall'] = age_overall


    def section_header(label):
        return pd.DataFrame(index=[f"{label}, n (%)"])

    def indent_index(df):
        df = df.copy()
        df.index = ['  ' + str(i) for i in df.index]
        return df

    sex_table = indent_index(sex_table)
    race_table = indent_index(race_table)
    age_table = indent_index(age_table)


    table1 = pd.concat(
        [
            section_header("Sex"),
            sex_table,
            section_header("Race"),
            race_table,
            section_header("Age Group"),
            age_table
        ]
    ).fillna("0 (0.0%)")
    
    condition_totals = pd.DataFrame(
    df_u.groupby(condition_column)['ssid']
        .nunique()
    ).reset_index().assign(ssid=lambda x: x['ssid'].apply("{:,}".format))

    return table1, condition_totals


## EXAMPLE USAGE ##
ccw_table1, ccw_totals = create_table1(ccw_df, 'condition')
