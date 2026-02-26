def calculate_or(df, groups, exposure, outcomes):
    tables = []
    results = []
    df_filtered = df[df[exposure].isin(groups)]
    
    for outcome in outcomes:
        ct = pd.crosstab(df_filtered[exposure], df_filtered[outcome])
        ct = ct.reindex(index=groups)
        if ct.shape != (2, 2):
            continue
        
        table = ct.values
        tables.append(table)
        
        exposure_levels = ct.index.tolist()    # e.g. ['A', 'B'] — row 0 vs row 1
        outcome_levels = ct.columns.tolist()   # e.g. [0, 1] or ['No', 'Yes']
        
        res = odds_ratio(table)
        ci = res.confidence_interval()
        
        results.append({
            'condition': outcome,
            'exposure_ref': exposure_levels[0],      # reference group (row 0)
            'exposure_comp': exposure_levels[1],     # comparison group (row 1)
            'outcome_ref': outcome_levels[0],        # reference outcome (col 0)
            'outcome_event': outcome_levels[1],      # event outcome (col 1)
            'comparison': f"{exposure_levels[0]} vs {exposure_levels[1]}",
            'interpretation': f"Odds of [{outcome_levels[1]}] in [{exposure_levels[0]}] vs [{exposure_levels[1]}]",
            'Odds Ratio': res.statistic,
            '95% CI': (ci.low, ci.high)
        })
    
    return tables, results
