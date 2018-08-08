Simple script to compare test results in jenkins. Detects disjoing sets of failing tests between two branches.

Sample usage:

    /jen_compare.py --base 'http://jenkins.host.example/job' --main 'main/7' --feature 'feature-xyz/42'
