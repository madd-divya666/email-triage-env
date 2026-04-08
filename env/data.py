"""
Email dataset with ground-truth labels for all 3 task difficulties.
Each email has:
  - easy_label:   urgent / not_urgent
  - medium_label: billing | technical_support | complaint | general_inquiry | spam
  - hard_label:   {category, priority (1-5), routing_department}
"""

EMAILS = [
    {
        "email_id": "E001",
        "sender": "sysalert@infra.company.com",
        "subject": "CRITICAL: Production database is down",
        "body": (
            "Our primary production database (db-prod-01) has been unreachable for the past 10 minutes. "
            "All customer-facing services are affected. Error: Connection timeout on port 5432. "
            "Immediate action required."
        ),
        "easy_label": "urgent",
        "medium_label": "technical_support",
        "hard_label": {"category": "technical_support", "priority": 1, "routing_department": "tech_team"},
    },
    {
        "email_id": "E002",
        "sender": "deals@newsletter.shop.com",
        "subject": "Weekend Sale — Up to 70% off everything!",
        "body": (
            "Hey there! Don't miss our biggest sale of the year. "
            "Shop electronics, fashion, home goods and more. Use code SAVE70 at checkout. "
            "Offer valid this weekend only. Unsubscribe anytime."
        ),
        "easy_label": "not_urgent",
        "medium_label": "spam",
        "hard_label": {"category": "spam", "priority": 5, "routing_department": "spam_filter"},
    },
    {
        "email_id": "E003",
        "sender": "john.carter@client.com",
        "subject": "Invoice #4821 — incorrect charges on my account",
        "body": (
            "Hi, I received my monthly invoice (#4821) and noticed I was charged $149 instead of $99 "
            "as per my subscription plan. This is the second time this has happened. "
            "Please correct the charge and issue a refund for the difference. "
            "I need this resolved before the 15th or I will dispute via my bank."
        ),
        "easy_label": "urgent",
        "medium_label": "billing",
        "hard_label": {"category": "billing", "priority": 2, "routing_department": "finance"},
    },
    {
        "email_id": "E004",
        "sender": "sarah.lee@gmail.com",
        "subject": "Question about your premium plan features",
        "body": (
            "Hello, I'm considering upgrading to your premium plan. "
            "Could you clarify whether it includes API access and how many team members I can add? "
            "Also, is there a free trial available? Thanks in advance."
        ),
        "easy_label": "not_urgent",
        "medium_label": "general_inquiry",
        "hard_label": {"category": "general_inquiry", "priority": 4, "routing_department": "general_support"},
    },
    {
        "email_id": "E005",
        "sender": "angry.customer@hotmail.com",
        "subject": "Absolutely terrible service — I want a refund",
        "body": (
            "I have been a customer for 3 years and the quality has gone completely downhill. "
            "My last three support tickets were closed without resolution. "
            "I was promised a callback that never happened. "
            "This is unacceptable. I want a full refund for this month and I'm considering leaving."
        ),
        "easy_label": "urgent",
        "medium_label": "complaint",
        "hard_label": {"category": "complaint", "priority": 2, "routing_department": "customer_relations"},
    },
    {
        "email_id": "E006",
        "sender": "no-reply@marketing.promo.biz",
        "subject": "You've been selected for an exclusive reward!",
        "body": (
            "Congratulations! You have been randomly selected to receive a $500 Amazon gift card. "
            "Click the link below to claim your reward within 24 hours. "
            "This offer is exclusively for you. Act fast!"
        ),
        "easy_label": "not_urgent",
        "medium_label": "spam",
        "hard_label": {"category": "spam", "priority": 5, "routing_department": "spam_filter"},
    },
    {
        "email_id": "E007",
        "sender": "mike.johnson@enterprise.com",
        "subject": "Cannot log in — account locked after password reset",
        "body": (
            "Hi support, I tried to reset my password this morning but after following the steps "
            "I am now getting an 'Account Locked' error. I have an important demo with a client in 2 hours "
            "and I cannot access the platform. Please help urgently. Ticket ref: none yet."
        ),
        "easy_label": "urgent",
        "medium_label": "technical_support",
        "hard_label": {"category": "technical_support", "priority": 1, "routing_department": "tech_team"},
    },
    {
        "email_id": "E008",
        "sender": "priya.sharma@startup.io",
        "subject": "Feedback on new dashboard — a few suggestions",
        "body": (
            "Hi team, I wanted to share some feedback on the new dashboard released last week. "
            "Overall it looks great! A couple of small suggestions: it would be helpful to have "
            "a date filter on the analytics page, and the export button is a bit hard to find. "
            "No rush, just thought it might help future improvements."
        ),
        "easy_label": "not_urgent",
        "medium_label": "general_inquiry",
        "hard_label": {"category": "general_inquiry", "priority": 5, "routing_department": "general_support"},
    },
    {
        "email_id": "E009",
        "sender": "accounts@bigcorp.com",
        "subject": "Payment declined — service suspension warning",
        "body": (
            "Dear customer, your payment of $299 due on April 1st was declined. "
            "Please update your payment method within 48 hours to avoid service suspension. "
            "Log in to your billing portal to update your card details."
        ),
        "easy_label": "urgent",
        "medium_label": "billing",
        "hard_label": {"category": "billing", "priority": 2, "routing_department": "finance"},
    },
    {
        "email_id": "E010",
        "sender": "unhappy.user@yahoo.com",
        "subject": "Your app keeps crashing on iOS 17 — totally unusable",
        "body": (
            "I updated to iOS 17 last week and your app crashes every time I try to open it. "
            "I've tried reinstalling three times. This has been going on for 5 days with no fix. "
            "Other users on your community forum are reporting the same issue. "
            "When will this be fixed? I'm paying for a service I cannot use."
        ),
        "easy_label": "urgent",
        "medium_label": "technical_support",
        "hard_label": {"category": "technical_support", "priority": 1, "routing_department": "tech_team"},
    },
]
