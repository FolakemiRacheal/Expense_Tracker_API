API Endpoints to Build

Here’s a detailed API plan, grouped logically:

A. Authentication & Users

POST /auth/register → Create new user

POST /auth/login → Login user, return JWT

POST /auth/logout → Revoke token

GET /users/me → Get user profile

PATCH /users/me → Update profile

DELETE /users/me → Delete account





B. Transactions

POST /transactions → Add expense/income

GET /transactions → Get all transactions with filters (category, date, tags, type)

GET /transactions/:id → Get single transaction

PATCH /transactions/:id → Update transaction

DELETE /transactions/:id → Delete transaction

C. Categories & Tags

GET /categories → List all categories

POST /categories → Add new category

PATCH /categories/:id → Update category

DELETE /categories/:id → Remove category

GET /tags → List all tags

POST /tags → Add tag

D. Budgets

POST /budgets → Create a budget

GET /budgets → List all budgets

GET /budgets/:id → Get budget summary

PATCH /budgets/:id → Update budget

DELETE /budgets/:id → Remove budget

E. Recurring Transactions

POST /recurring-transactions → Create recurring

GET /recurring-transactions → List recurring transactions

PATCH /recurring-transactions/:id → Update

DELETE /recurring-transactions/:id → Remove

F. Analytics & Insights

GET /analytics/summary → Summary by day/week/month/year

GET /analytics/category-trends → Spending per category

GET /analytics/forecast → Predicted expenses

GET /analytics/alerts → Overspending alerts

G. Advanced (Optional for Senior-Level)

POST /receipts/upload → Upload receipt for OCR parsing

POST /transactions/split → Create split transaction

GET /currencies → Supported currencies & rates

POST /notifications → Configure notification preferences

GET /export → Export transactions (CSV/PDF/Excel)










RECEIPT MODEL — FIELD-BY-FIELD DEEP DIVE
1️⃣ status
status = models.CharField(max_length=20, default="pending")

What it represents

The current processing state of the receipt.

Why it exists

Receipt processing is asynchronous (OCR happens in background jobs).
You need to track where the receipt is in the pipeline.

Typical lifecycle
pending → processing → processed
              ↘
               failed

Common values

pending – Uploaded, not processed yet

processing – OCR task running

processed – Successfully parsed

failed – OCR error / unreadable receipt

Best practice (VERY IMPORTANT)

Use choices, not free text:

STATUS_CHOICES = (
    ("pending", "Pending"),
    ("processing", "Processing"),
    ("processed", "Processed"),
    ("failed", "Failed"),
)

status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default="pending"
)

Business logic usage

Frontend shows loading states

Retry OCR on failed

Prevent linking transaction until processed

2️⃣ parsed_amount
parsed_amount = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    null=True
)

What it represents

The amount extracted from the receipt by OCR.

Why it exists

OCR isn’t always perfect — users must:

Review extracted values

Confirm or correct them

Why DecimalField

Money must be:

Precise

Non-floating

Why null=True

OCR may fail

Amount might not be detected

Example values

12500.00

null (OCR failed)

Business logic usage

Pre-fill transaction amount

User confirmation step

3️⃣ parsed_date
parsed_date = models.DateField(null=True)

What it represents

The transaction date detected from the receipt.

Why it exists

Receipts often show:

Purchase date

Invoice date

This allows:

Accurate historical records

Backdated transactions

Why null=True

Date may be missing

OCR may not detect it

Business logic usage

Default transaction date

Editable by user

4️⃣ merchant_name
merchant_name = models.CharField(max_length=100, null=True)

What it represents

The vendor/store name extracted from the receipt.

Examples

Shoprite

Amazon

Uber

KFC

Why it exists

Analytics (top merchants)

Better transaction labeling

Search & filters

Why null=True

OCR may not detect merchant

Some receipts don’t include vendor names

Best practice

Later, you can normalize this into a Merchant model, but for now:
✔ Simple
✔ Flexible

5️⃣ transaction
transaction = models.ForeignKey(
    "transactions.Transaction",
    on_delete=models.SET_NULL,
    null=True
)

What it represents

Links the receipt to the actual transaction record.

Why it exists

Receipts don’t always create transactions automatically.

Possible flows:

Upload receipt → parse → user confirms → transaction created

Upload receipt → attach to existing transaction

Why SET_NULL

If a transaction is deleted:

Receipt should still exist

Avoid data loss

Why null=True

Receipt may exist before transaction creation

Business logic usage

One receipt → one transaction

Prevent multiple links

6️⃣ uploaded_at
uploaded_at = models.DateTimeField(auto_now_add=True)

What it represents

When the receipt was uploaded.

Why it exists

Sorting

Debugging

Audit logs

Business logic usage

Show upload history

Cleanup old failed receipts

✅ FULL IMPROVED RECEIPT MODEL (PRODUCTION-READY)
class Receipt(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("processed", "Processed"),
        ("failed", "Failed"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="receipts"
    )

    image = models.ImageField(upload_to="receipts/")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    parsed_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    parsed_date = models.DateField(
        null=True,
        blank=True
    )

    merchant_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    transaction = models.ForeignKey(
        "transactions.Transaction",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt {self.id} - {self.status}"

🧠 INTERVIEW-LEVEL EXPLANATION

“Receipt processing is asynchronous, so we introduced a status field to track OCR progress. Parsed fields are nullable to handle OCR uncertainty, and receipts are loosely coupled to transactions to support flexible workflows.”

🔥 NEXT STEP OPTIONS

I can:
1️⃣ Design OCR Celery task flow
2️⃣ Add retry & error handling
3️⃣ Show how receipt → transaction conversion works

Tell me which one you want 👌















🚀 POST-MODEL DAY-BY-DAY BACKEND PLAN
🔹 DAY 1 – Serializers & Validation Layer

Goal: Control how data enters and leaves your system

<!-- Tasks

Create serializers for each app:

User / Profile

Category

Transaction

Receipt

Budget

Notification

Add field-level validations:

Amount must be > 0

Category type must match transaction type

Budget limit must be positive

Use SerializerMethodField where needed

Output

✔ Clean data contracts
✔ Predictable API responses

🔹 DAY 2 – Authentication & Permissions

Goal: Lock down your API properly

Tasks

Configure authentication:

JWT (recommended) or Session Auth

Ensure per-user data isolation:

Users only see their own transactions

Users only edit their own categories/budgets

Create custom permissions:

IsOwner
IsNotDefaultCategory

Output -->

✔ Secure API
✔ Interview-ready permission logic

🔹 DAY 3 – CRUD APIs (ViewSets)

Goal: Make your system usable

Tasks

Build ViewSets for:

Categories

Transactions

Receipts

Budgets

Notifications

Add:

Filtering

Searching

Ordering

Soft-delete where necessary (optional)

Output

✔ Fully usable API
✔ Consistent REST structure

🔹 DAY 4 – Business Rules & Edge Cases

Goal: Enforce correctness

Tasks

Prevent:

Deleting default categories

Editing another user’s data

Mismatched income/expense categories

Validate:

Split transactions total = parent amount

One budget per category per user

Add database constraints where needed

Output

✔ Strong data integrity
✔ Fewer bugs

🔹 DAY 5 – Analytics (Service Layer)

Goal: Convert data → insights

Tasks

Create analytics services:

Monthly summaries

Category breakdowns

Spending trends

No heavy models — use querysets

Expose analytics endpoints:

GET /analytics/monthly-summary
GET /analytics/category-breakdown

Output

✔ Business-value endpoints
✔ Recruiter-friendly feature

🔹 DAY 6 – PostgreSQL Optimization & Indexing

Goal: Performance & scalability

Tasks

Add indexes to:

transaction_date

category

user

Review query performance

Ensure migrations are clean

Output

✔ Fast queries
✔ Production-grade DB setup

🔹 DAY 7 – Testing

Goal: Prove your code works

Tasks

Unit tests for:

Models

Permissions

Serializers

API tests:

Create transaction

Prevent unauthorized access

Test PostgreSQL-specific behavior

Output

✔ Confidence
✔ Professional credibility

🔹 DAY 8 – Documentation

Goal: Make it usable by others

Tasks

Swagger / OpenAPI docs

Clear endpoint descriptions

Example request & responses

Output

✔ API others can consume
✔ Strong portfolio signal

🔹 DAY 9 – Error Handling & Logging

Goal: Production readiness

Tasks

Standardize error responses

Handle constraint violations cleanly

Add logging for:

Failed transactions

Receipt parsing failures

Output

✔ Debuggable system
✔ Real-world robustness

🔹 DAY 10 – Deployment Prep

Goal: Ship mindset

Tasks

Environment variables review

.env separation

Gunicorn + Whitenoise

Prepare for Docker (optional)

Output

✔ Deployable backend
✔ Ready for real users