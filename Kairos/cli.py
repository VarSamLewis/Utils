import argparse
from Kairos.Kairos import provide_guidance

def summon_kairos():
    parser = argparse.ArgumentParser(description="CLI LLM that roleplays as Kairos Fateweaver")
    parser.add_argument("query", help="Query for which you seek guidance")
    args = parser.parse_args()
    provide_guidance(args.query)
