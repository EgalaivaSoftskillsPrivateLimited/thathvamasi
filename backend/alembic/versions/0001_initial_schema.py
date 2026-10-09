"""Initial PostgreSQL schema for Thathvamasi HR Consultancy

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-10-05 17:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. users
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('designation', sa.String(length=100), nullable=True),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('avatar_url', sa.String(length=500), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('is_verified', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('role', sa.String(length=50), server_default='user', nullable=False),
        sa.Column('permissions', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
        sa.Column('verification_token', sa.String(length=255), nullable=True),
        sa.Column('reset_token', sa.String(length=255), nullable=True),
        sa.Column('reset_token_expires', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('login_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('failed_login_attempts', sa.Integer(), server_default='0', nullable=False),
        sa.Column('locked_until', sa.DateTime(timezone=True), nullable=True),
        sa.Column('preferences', postgresql.JSON(astext_type=sa.Text()), server_default='{}', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email', name='uq_users_email')
    )
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_users_role', 'users', ['role'])
    op.create_index('ix_users_is_active', 'users', ['is_active'])
    op.create_index('ix_users_created_at', 'users', ['created_at'])

    # 2. user_activities
    op.create_table(
        'user_activities',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('activity_type', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('activity_metadata', postgresql.JSON(astext_type=sa.Text()), server_default='{}', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_activities_user_id', 'user_activities', ['user_id'])
    op.create_index('ix_user_activities_activity_type', 'user_activities', ['activity_type'])
    op.create_index('ix_user_activities_created_at', 'user_activities', ['created_at'])
    op.create_index('ix_user_activities_user_id_created_at', 'user_activities', ['user_id', 'created_at'])

    # 3. candidates
    op.create_table(
        'candidates',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('status', sa.String(length=50), server_default='new', nullable=False),
        sa.Column('status_changed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status_notes', sa.Text(), nullable=True),
        sa.Column('assigned_to', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('priority', sa.String(length=20), server_default='medium', nullable=False),
        sa.Column('tags', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
        sa.Column('consent_accepted', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('consent_accepted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('source', sa.String(length=100), nullable=True),
        sa.Column('referrer', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['assigned_to'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_candidates_status', 'candidates', ['status'])
    op.create_index('ix_candidates_created_at', 'candidates', ['created_at'])
    op.create_index('ix_candidates_assigned_to', 'candidates', ['assigned_to'])
    op.create_index('ix_candidates_priority', 'candidates', ['priority'])
    op.create_index('ix_candidates_source', 'candidates', ['source'])

    # 4. candidate_personal_details
    op.create_table(
        'candidate_personal_details',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('candidate_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('mobile', sa.String(length=20), nullable=False),
        sa.Column('whatsapp', sa.String(length=20), nullable=True),
        sa.Column('current_location', sa.String(length=255), nullable=False),
        sa.Column('preferred_location', sa.String(length=255), nullable=True),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.Column('gender', sa.String(length=20), nullable=True),
        sa.Column('marital_status', sa.String(length=20), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('state', sa.String(length=100), nullable=True),
        sa.Column('country', sa.String(length=100), server_default='India', nullable=False),
        sa.Column('pincode', sa.String(length=10), nullable=True),
        sa.Column('emergency_contact_name', sa.String(length=255), nullable=True),
        sa.Column('emergency_contact_phone', sa.String(length=20), nullable=True),
        sa.Column('emergency_contact_relation', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('candidate_id')
    )
    op.create_index('ix_candidate_personal_details_email', 'candidate_personal_details', ['email'])
    op.create_index('ix_candidate_personal_details_mobile', 'candidate_personal_details', ['mobile'])
    op.create_index('ix_candidate_personal_details_location', 'candidate_personal_details', ['current_location'])

    # 5. candidate_professional_details
    op.create_table(
        'candidate_professional_details',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('candidate_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('highest_qualification', sa.String(length=255), nullable=False),
        sa.Column('specialization', sa.String(length=255), nullable=True),
        sa.Column('university', sa.String(length=255), nullable=True),
        sa.Column('graduation_year', sa.Integer(), nullable=True),
        sa.Column('total_experience', sa.String(length=50), nullable=False),
        sa.Column('years_of_experience', sa.Float(), nullable=True),
        sa.Column('current_company', sa.String(length=255), nullable=True),
        sa.Column('current_designation', sa.String(length=255), nullable=True),
        sa.Column('current_salary', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('current_salary_currency', sa.String(length=10), server_default='INR', nullable=False),
        sa.Column('expected_salary', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('expected_salary_currency', sa.String(length=10), server_default='INR', nullable=False),
        sa.Column('notice_period', sa.String(length=50), nullable=True),
        sa.Column('notice_period_days', sa.Integer(), nullable=True),
        sa.Column('skills', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
        sa.Column('preferred_job_role', sa.String(length=255), nullable=True),
        sa.Column('preferred_industry', sa.String(length=255), nullable=True),
        sa.Column('job_type_preference', sa.String(length=50), nullable=True),
        sa.Column('work_preference', sa.String(length=50), nullable=True),
        sa.Column('languages_known', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
        sa.Column('certifications', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
        sa.Column('achievements', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('candidate_id')
    )
    op.create_index('ix_candidate_professional_details_skills', 'candidate_professional_details', ['skills'], postgresql_using='gin')
    op.create_index('ix_candidate_professional_details_experience', 'candidate_professional_details', ['years_of_experience'])
    op.create_index('ix_candidate_professional_details_qualification', 'candidate_professional_details', ['highest_qualification'])

    # 6. candidate_resumes
    op.create_table(
        'candidate_resumes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('candidate_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('file_url', sa.String(length=500), nullable=False),
        sa.Column('file_name', sa.String(length=255), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('file_type', sa.String(length=50), nullable=False),
        sa.Column('cloudinary_id', sa.String(length=255), nullable=True),
        sa.Column('version', sa.Integer(), server_default='1', nullable=False),
        sa.Column('is_primary', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('uploaded_by', sa.String(length=255), nullable=True),
        sa.Column('is_parsed', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('parsed_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_candidate_resumes_candidate_id', 'candidate_resumes', ['candidate_id'])
    op.create_index('ix_candidate_resumes_is_primary', 'candidate_resumes', ['is_primary'])
    op.create_index('ix_candidate_resumes_uploaded_at', 'candidate_resumes', ['uploaded_at'])

    # 7. candidate_metadata
    op.create_table(
        'candidate_metadata',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('candidate_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('device_type', sa.String(length=50), nullable=True),
        sa.Column('browser', sa.String(length=50), nullable=True),
        sa.Column('operating_system', sa.String(length=50), nullable=True),
        sa.Column('referrer_url', sa.String(length=500), nullable=True),
        sa.Column('landing_page', sa.String(length=500), nullable=True),
        sa.Column('utm_source', sa.String(length=100), nullable=True),
        sa.Column('utm_medium', sa.String(length=100), nullable=True),
        sa.Column('utm_campaign', sa.String(length=100), nullable=True),
        sa.Column('utm_term', sa.String(length=100), nullable=True),
        sa.Column('utm_content', sa.String(length=100), nullable=True),
        sa.Column('form_version', sa.String(length=50), nullable=True),
        sa.Column('form_fields', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('candidate_id')
    )

    # 8. candidate_work_experiences
    op.create_table(
        'candidate_work_experiences',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('professional_details_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company_name', sa.String(length=255), nullable=False),
        sa.Column('company_industry', sa.String(length=255), nullable=True),
        sa.Column('company_size', sa.String(length=50), nullable=True),
        sa.Column('designation', sa.String(length=255), nullable=False),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('employment_type', sa.String(length=50), server_default='full_time', nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('is_current', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('work_mode', sa.String(length=50), nullable=True),
        sa.Column('responsibilities', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
        sa.Column('achievements', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
        sa.Column('salary', sa.Float(), nullable=True),
        sa.Column('salary_currency', sa.String(length=10), server_default='INR', nullable=False),
        sa.Column('reason_for_leaving', sa.String(length=255), nullable=True),
        sa.Column('references', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['professional_details_id'], ['candidate_professional_details.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_candidate_work_experiences_company', 'candidate_work_experiences', ['company_name'])
    op.create_index('ix_candidate_work_experiences_designation', 'candidate_work_experiences', ['designation'])
    op.create_index('ix_candidate_work_experiences_dates', 'candidate_work_experiences', ['start_date', 'end_date'])

    # 9. candidate_educations
    op.create_table(
        'candidate_educations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('professional_details_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('institution_name', sa.String(length=255), nullable=False),
        sa.Column('institution_type', sa.String(length=50), nullable=True),
        sa.Column('institution_location', sa.String(length=255), nullable=True),
        sa.Column('qualification', sa.String(length=255), nullable=False),
        sa.Column('specialization', sa.String(length=255), nullable=True),
        sa.Column('degree_type', sa.String(length=50), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('is_completed', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('grade', sa.String(length=20), nullable=True),
        sa.Column('score', sa.Float(), nullable=True),
        sa.Column('max_score', sa.Float(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('achievements', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['professional_details_id'], ['candidate_professional_details.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_candidate_educations_institution', 'candidate_educations', ['institution_name'])
    op.create_index('ix_candidate_educations_qualification', 'candidate_educations', ['qualification'])

    # 10. candidate_notes
    op.create_table(
        'candidate_notes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('candidate_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('note_type', sa.String(length=50), server_default='general', nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('is_private', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_candidate_notes_candidate_id', 'candidate_notes', ['candidate_id'])
    op.create_index('ix_candidate_notes_created_at', 'candidate_notes', ['created_at'])
    op.create_index('ix_candidate_notes_note_type', 'candidate_notes', ['note_type'])

    # 11. candidate_interviews
    op.create_table(
        'candidate_interviews',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('candidate_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('interview_type', sa.String(length=50), nullable=False),
        sa.Column('interview_stage', sa.String(length=50), nullable=False),
        sa.Column('scheduled_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), server_default='60', nullable=False),
        sa.Column('timezone', sa.String(length=50), server_default='Asia/Kolkata', nullable=False),
        sa.Column('interviewer_ids', sa.ARRAY(postgresql.UUID(as_uuid=True)), server_default='{}', nullable=False),
        sa.Column('interviewer_names', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
        sa.Column('meeting_link', sa.String(length=500), nullable=True),
        sa.Column('meeting_platform', sa.String(length=50), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('status', sa.String(length=50), server_default='scheduled', nullable=False),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_candidate_interviews_candidate_id', 'candidate_interviews', ['candidate_id'])
    op.create_index('ix_candidate_interviews_scheduled_at', 'candidate_interviews', ['scheduled_at'])
    op.create_index('ix_candidate_interviews_status', 'candidate_interviews', ['status'])
    op.create_index('ix_candidate_interviews_interview_stage', 'candidate_interviews', ['interview_stage'])

    # 12. clients
    op.create_table(
        'clients',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('company_name', sa.String(length=255), nullable=False),
        sa.Column('company_email', sa.String(length=255), nullable=False),
        sa.Column('company_phone', sa.String(length=20), nullable=True),
        sa.Column('company_website', sa.String(length=500), nullable=True),
        sa.Column('contact_person_name', sa.String(length=255), nullable=False),
        sa.Column('contact_person_email', sa.String(length=255), nullable=False),
        sa.Column('contact_person_phone', sa.String(length=20), nullable=False),
        sa.Column('contact_person_designation', sa.String(length=100), nullable=True),
        sa.Column('company_size', sa.String(length=50), nullable=True),
        sa.Column('company_type', sa.String(length=50), nullable=True),
        sa.Column('industry', sa.String(length=255), nullable=True),
        sa.Column('headquarters', sa.String(length=255), nullable=True),
        sa.Column('company_address', sa.Text(), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('state', sa.String(length=100), nullable=True),
        sa.Column('country', sa.String(length=100), server_default='India', nullable=False),
        sa.Column('pincode', sa.String(length=10), nullable=True),
        sa.Column('status', sa.String(length=50), server_default='new', nullable=False),
        sa.Column('status_changed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status_notes', sa.Text(), nullable=True),
        sa.Column('assigned_to', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('account_manager', sa.String(length=255), nullable=True),
        sa.Column('client_type', sa.String(length=50), server_default='regular', nullable=False),
        sa.Column('tags', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
        sa.Column('billing_name', sa.String(length=255), nullable=True),
        sa.Column('billing_email', sa.String(length=255), nullable=True),
        sa.Column('billing_phone', sa.String(length=20), nullable=True),
        sa.Column('billing_address', sa.Text(), nullable=True),
        sa.Column('gst_number', sa.String(length=50), nullable=True),
        sa.Column('pan_number', sa.String(length=50), nullable=True),
        sa.Column('source', sa.String(length=100), nullable=True),
        sa.Column('referrer', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['assigned_to'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_clients_company_name', 'clients', ['company_name'])
    op.create_index('ix_clients_company_email', 'clients', ['company_email'])
    op.create_index('ix_clients_status', 'clients', ['status'])
    op.create_index('ix_clients_client_type', 'clients', ['client_type'])
    op.create_index('ix_clients_created_at', 'clients', ['created_at'])
    op.create_index('ix_clients_assigned_to', 'clients', ['assigned_to'])

    # 13. hiring_requirements
    op.create_table(
        'hiring_requirements',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('client_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('position_title', sa.String(length=255), nullable=False),
        sa.Column('number_of_vacancies', sa.Integer(), server_default='1', nullable=False),
        sa.Column('job_location', sa.String(length=255), nullable=False),
        sa.Column('required_experience', sa.String(length=100), nullable=True),
        sa.Column('required_qualification', sa.String(length=255), nullable=True),
        sa.Column('key_skills', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
        sa.Column('salary_range_min', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('salary_range_max', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('salary_currency', sa.String(length=10), server_default='INR', nullable=False),
        sa.Column('salary_type', sa.String(length=50), nullable=True),
        sa.Column('employment_type', sa.String(length=50), server_default='permanent', nullable=False),
        sa.Column('work_mode', sa.String(length=50), nullable=True),
        sa.Column('shift_timing', sa.String(length=100), nullable=True),
        sa.Column('expected_joining_timeline', sa.String(length=100), nullable=True),
        sa.Column('deadline', sa.Date(), nullable=True),
        sa.Column('job_description', sa.Text(), nullable=True),
        sa.Column('additional_requirements', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), server_default='open', nullable=False),
        sa.Column('status_changed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status_notes', sa.Text(), nullable=True),
        sa.Column('priority', sa.String(length=20), server_default='medium', nullable=False),
        sa.Column('assigned_to', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['assigned_to'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_hiring_requirements_client_id', 'hiring_requirements', ['client_id'])
    op.create_index('ix_hiring_requirements_status', 'hiring_requirements', ['status'])
    op.create_index('ix_hiring_requirements_position_title', 'hiring_requirements', ['position_title'])
    op.create_index('ix_hiring_requirements_priority', 'hiring_requirements', ['priority'])
    op.create_index('ix_hiring_requirements_created_at', 'hiring_requirements', ['created_at'])

    # 14. job_description_documents
    op.create_table(
        'job_description_documents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('hiring_requirement_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('file_url', sa.String(length=500), nullable=False),
        sa.Column('file_name', sa.String(length=255), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('file_type', sa.String(length=50), nullable=False),
        sa.Column('cloudinary_id', sa.String(length=255), nullable=True),
        sa.Column('version', sa.Integer(), server_default='1', nullable=False),
        sa.Column('is_primary', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('uploaded_by', sa.String(length=255), nullable=True),
        sa.Column('is_parsed', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('parsed_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['hiring_requirement_id'], ['hiring_requirements.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_job_description_documents_hiring_requirement_id', 'job_description_documents', ['hiring_requirement_id'])
    op.create_index('ix_job_description_documents_is_primary', 'job_description_documents', ['is_primary'])

    # 15. client_contacts
    op.create_table(
        'client_contacts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('client_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('designation', sa.String(length=100), nullable=True),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=False),
        sa.Column('is_primary', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_client_contacts_client_id', 'client_contacts', ['client_id'])
    op.create_index('ix_client_contacts_is_primary', 'client_contacts', ['is_primary'])
    op.create_index('ix_client_contacts_name', 'client_contacts', ['name'])

    # 16. client_documents
    op.create_table(
        'client_documents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('client_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('document_name', sa.String(length=255), nullable=False),
        sa.Column('document_type', sa.String(length=50), nullable=False),
        sa.Column('file_url', sa.String(length=500), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('file_type', sa.String(length=50), nullable=False),
        sa.Column('cloudinary_id', sa.String(length=255), nullable=True),
        sa.Column('version', sa.Integer(), server_default='1', nullable=False),
        sa.Column('status', sa.String(length=50), server_default='active', nullable=False),
        sa.Column('expiry_date', sa.Date(), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('uploaded_by', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_client_documents_client_id', 'client_documents', ['client_id'])
    op.create_index('ix_client_documents_document_type', 'client_documents', ['document_type'])
    op.create_index('ix_client_documents_status', 'client_documents', ['status'])

    # 17. client_metadata
    op.create_table(
        'client_metadata',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('client_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('device_type', sa.String(length=50), nullable=True),
        sa.Column('browser', sa.String(length=50), nullable=True),
        sa.Column('operating_system', sa.String(length=50), nullable=True),
        sa.Column('referrer_url', sa.String(length=500), nullable=True),
        sa.Column('landing_page', sa.String(length=500), nullable=True),
        sa.Column('utm_source', sa.String(length=100), nullable=True),
        sa.Column('utm_medium', sa.String(length=100), nullable=True),
        sa.Column('utm_campaign', sa.String(length=100), nullable=True),
        sa.Column('utm_term', sa.String(length=100), nullable=True),
        sa.Column('utm_content', sa.String(length=100), nullable=True),
        sa.Column('form_version', sa.String(length=50), nullable=True),
        sa.Column('form_fields', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('client_id')
    )

    # 18. client_notes
    op.create_table(
        'client_notes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('client_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('note_type', sa.String(length=50), server_default='general', nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('is_private', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_client_notes_client_id', 'client_notes', ['client_id'])
    op.create_index('ix_client_notes_created_at', 'client_notes', ['created_at'])
    op.create_index('ix_client_notes_note_type', 'client_notes', ['note_type'])

    # 19. client_meetings
    op.create_table(
        'client_meetings',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('client_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('meeting_type', sa.String(length=50), nullable=False),
        sa.Column('scheduled_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), server_default='60', nullable=False),
        sa.Column('timezone', sa.String(length=50), server_default='Asia/Kolkata', nullable=False),
        sa.Column('attendees', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
        sa.Column('meeting_link', sa.String(length=500), nullable=True),
        sa.Column('meeting_platform', sa.String(length=50), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('status', sa.String(length=50), server_default='scheduled', nullable=False),
        sa.Column('agenda', sa.Text(), nullable=True),
        sa.Column('minutes_of_meeting', sa.Text(), nullable=True),
        sa.Column('action_items', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_client_meetings_client_id', 'client_meetings', ['client_id'])
    op.create_index('ix_client_meetings_scheduled_at', 'client_meetings', ['scheduled_at'])
    op.create_index('ix_client_meetings_status', 'client_meetings', ['status'])
    op.create_index('ix_client_meetings_meeting_type', 'client_meetings', ['meeting_type'])

    # 20. hiring_requirement_candidates
    op.create_table(
        'hiring_requirement_candidates',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('hiring_requirement_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('candidate_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.String(length=50), server_default='shortlisted', nullable=False),
        sa.Column('match_score', sa.Float(), nullable=True),
        sa.Column('matching_skills', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
        sa.Column('missing_skills', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('assigned_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('assigned_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('status_changed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['assigned_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['hiring_requirement_id'], ['hiring_requirements.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('hiring_requirement_id', 'candidate_id', name='uq_hiring_requirement_candidate')
    )
    op.create_index('ix_hiring_requirement_candidates_hiring_requirement_id', 'hiring_requirement_candidates', ['hiring_requirement_id'])
    op.create_index('ix_hiring_requirement_candidates_candidate_id', 'hiring_requirement_candidates', ['candidate_id'])
    op.create_index('ix_hiring_requirement_candidates_status', 'hiring_requirement_candidates', ['status'])
    op.create_index('ix_hiring_requirement_candidates_match_score', 'hiring_requirement_candidates', ['match_score'])

    # 21. blogs
    op.create_table(
        'blogs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('excerpt', sa.Text(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('author_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('author_name', sa.String(length=255), nullable=False),
        sa.Column('author_bio', sa.Text(), nullable=True),
        sa.Column('author_avatar', sa.String(length=500), nullable=True),
        sa.Column('categories', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
        sa.Column('tags', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
        sa.Column('is_published', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_featured', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('is_pinned', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('meta_title', sa.String(length=255), nullable=True),
        sa.Column('meta_description', sa.Text(), nullable=True),
        sa.Column('meta_keywords', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
        sa.Column('og_image_url', sa.String(length=500), nullable=True),
        sa.Column('canonical_url', sa.String(length=500), nullable=True),
        sa.Column('view_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('share_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('comment_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('like_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('read_time_minutes', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug', name='uq_blogs_slug')
    )
    op.create_index('ix_blogs_slug', 'blogs', ['slug'], unique=True)
    op.create_index('ix_blogs_is_published', 'blogs', ['is_published'])
    op.create_index('ix_blogs_published_at', 'blogs', ['published_at'])
    op.create_index('ix_blogs_is_featured', 'blogs', ['is_featured'])
    op.create_index('ix_blogs_categories', 'blogs', ['categories'], postgresql_using='gin')
    op.create_index('ix_blogs_tags', 'blogs', ['tags'], postgresql_using='gin')

    # 22. blog_images
    op.create_table(
        'blog_images',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('blog_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('image_url', sa.String(length=500), nullable=False),
        sa.Column('thumbnail_url', sa.String(length=500), nullable=True),
        sa.Column('original_filename', sa.String(length=255), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('file_type', sa.String(length=50), nullable=False),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('caption', sa.String(length=255), nullable=True),
        sa.Column('alt_text', sa.String(length=255), nullable=True),
        sa.Column('is_featured', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('display_order', sa.Integer(), server_default='0', nullable=False),
        sa.Column('cloudinary_id', sa.String(length=255), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['blog_id'], ['blogs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_blog_images_blog_id', 'blog_images', ['blog_id'])
    op.create_index('ix_blog_images_is_featured', 'blog_images', ['is_featured'])

    # 23. blog_comments
    op.create_table(
        'blog_comments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('blog_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('author_name', sa.String(length=255), nullable=False),
        sa.Column('author_email', sa.String(length=255), nullable=False),
        sa.Column('author_website', sa.String(length=500), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('is_approved', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('approved_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('parent_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['approved_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['blog_id'], ['blogs.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_id'], ['blog_comments.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_blog_comments_blog_id', 'blog_comments', ['blog_id'])
    op.create_index('ix_blog_comments_is_approved', 'blog_comments', ['is_approved'])
    op.create_index('ix_blog_comments_parent_id', 'blog_comments', ['parent_id'])
    op.create_index('ix_blog_comments_created_at', 'blog_comments', ['created_at'])

    # 24. blog_categories
    op.create_table(
        'blog_categories',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('post_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', name='uq_blog_categories_name'),
        sa.UniqueConstraint('slug', name='uq_blog_categories_slug')
    )
    op.create_index('ix_blog_categories_name', 'blog_categories', ['name'], unique=True)
    op.create_index('ix_blog_categories_slug', 'blog_categories', ['slug'], unique=True)
    op.create_index('ix_blog_categories_post_count', 'blog_categories', ['post_count'])

    # 25. blog_tags
    op.create_table(
        'blog_tags',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('post_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', name='uq_blog_tags_name'),
        sa.UniqueConstraint('slug', name='uq_blog_tags_slug')
    )
    op.create_index('ix_blog_tags_name', 'blog_tags', ['name'], unique=True)
    op.create_index('ix_blog_tags_slug', 'blog_tags', ['slug'], unique=True)
    op.create_index('ix_blog_tags_post_count', 'blog_tags', ['post_count'])


def downgrade() -> None:
    # Drop in reverse order of creation
    op.drop_table('blog_tags')
    op.drop_table('blog_categories')
    op.drop_table('blog_comments')
    op.drop_table('blog_images')
    op.drop_table('blogs')
    op.drop_table('hiring_requirement_candidates')
    op.drop_table('client_meetings')
    op.drop_table('client_notes')
    op.drop_table('client_metadata')
    op.drop_table('client_documents')
    op.drop_table('client_contacts')
    op.drop_table('job_description_documents')
    op.drop_table('hiring_requirements')
    op.drop_table('clients')
    op.drop_table('candidate_interviews')
    op.drop_table('candidate_notes')
    op.drop_table('candidate_educations')
    op.drop_table('candidate_work_experiences')
    op.drop_table('candidate_metadata')
    op.drop_table('candidate_resumes')
    op.drop_table('candidate_professional_details')
    op.drop_table('candidate_personal_details')
    op.drop_table('candidates')
    op.drop_table('user_activities')
    op.drop_table('users')
