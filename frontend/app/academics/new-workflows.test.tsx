import type { ReactNode } from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import NewLogbookEntryPage from './logbook/new/page';
import NewEvaluationPage from './evaluations/new/page';
import { academicsApi } from '@/lib/api/academics';

const push = jest.fn();
jest.mock('next/navigation', () => ({ useRouter: () => ({ push }) }));
jest.mock('@/components/auth/ProtectedRoute', () => ({ __esModule: true, default: ({ children }: { children: ReactNode }) => <>{children}</> }));
jest.mock('@/lib/api/academics', () => ({
  academicsApi: {
    listLogbookCategories: jest.fn(), listEvaluationTemplates: jest.fn(), getOptions: jest.fn(),
    createLogbookEntry: jest.fn(), submitLogbookEntry: jest.fn(),
    createEvaluationSubmission: jest.fn(), submitEvaluation: jest.fn(),
  },
}));
const api = academicsApi as unknown as Record<string, jest.Mock>;
const options = { supervisors: [{ id: 2, name: 'Dr Supervisor' }], periods: [{ id: 3, name: 'Term one' }] };

beforeEach(() => {
  jest.clearAllMocks();
  api.getOptions.mockResolvedValue(options);
  api.listLogbookCategories.mockResolvedValue([{ id: 1, name: 'Procedure', code: 'PROC', category_type: 'PROCEDURE' }]);
  api.listEvaluationTemplates.mockResolvedValue([{ id: 4, name: 'Mini CEX', form_type: 'MINI_CEX', schema: { fields: [{ key: 'score', label: 'Score', type: 'number', min: 1, max: 10 }, { key: 'feedback', label: 'Feedback', type: 'text' }] } }]);
  api.createLogbookEntry.mockResolvedValue({ id: 10 });
  api.submitLogbookEntry.mockResolvedValue({ id: 10, status: 'SUBMITTED' });
  api.createEvaluationSubmission.mockResolvedValue({ id: 11 });
  api.submitEvaluation.mockResolvedValue({ id: 11, status: 'SUBMITTED' });
});

describe('resident academic authoring forms', () => {
  it('validates required logbook fields before any request', async () => {
    render(<NewLogbookEntryPage />);
    await screen.findByRole('option', { name: /Procedure/ });
    fireEvent.click(screen.getByRole('button', { name: 'Save Draft' }));
    expect(screen.getByText('Please select a category.')).toBeInTheDocument();
    fireEvent.change(screen.getByDisplayValue('Choose a Category'), { target: { value: '1' } });
    fireEvent.click(screen.getByRole('button', { name: 'Save Draft' }));
    expect(screen.getByText('Please enter a title.')).toBeInTheDocument();
    expect(api.createLogbookEntry).not.toHaveBeenCalled();
  });

  it('maps procedure logbook details and submits the created entry', async () => {
    render(<NewLogbookEntryPage />);
    await screen.findByRole('option', { name: /Procedure/ });
    fireEvent.change(screen.getByDisplayValue('Choose a Category'), { target: { value: '1' } });
    fireEvent.change(screen.getByDisplayValue('Primary Supervisor / Verifier'), { target: { value: '2' } });
    fireEvent.change(screen.getByDisplayValue('Choose Period'), { target: { value: '3' } });
    fireEvent.change(screen.getByPlaceholderText('e.g. Ultrasound-guided central line'), { target: { value: 'Central line' } });
    fireEvent.change(screen.getByPlaceholderText('e.g. Central Venous Catheterization'), { target: { value: 'CVC' } });
    fireEvent.change(screen.getByPlaceholderText('e.g. CPT-36556'), { target: { value: 'CVC-1' } });
    fireEvent.change(screen.getByDisplayValue('Performed Under Supervision'), { target: { value: 'PERFORMED_INDEPENDENTLY' } });
    fireEvent.click(screen.getByRole('button', { name: 'Submit for Verification' }));
    await waitFor(() => expect(api.createLogbookEntry).toHaveBeenCalledWith(expect.objectContaining({ category: 1, supervisor: 2, academic_period: 3, title: 'Central line', procedure_record: expect.objectContaining({ procedure_name: 'CVC', procedure_code: 'CVC-1', role_performed: 'PERFORMED_INDEPENDENTLY' }) })));
    expect(api.submitLogbookEntry).toHaveBeenCalledWith(10);
    expect(await screen.findByText('Logbook entry submitted successfully.')).toBeInTheDocument();
  });

  it('maps typed and numeric evaluation responses and supports a draft', async () => {
    render(<NewEvaluationPage />);
    await screen.findByRole('option', { name: /Mini CEX/ });
    fireEvent.click(screen.getByRole('button', { name: 'Save Draft' }));
    expect(screen.getByText('Please select a template.')).toBeInTheDocument();
    fireEvent.change(screen.getByDisplayValue('Choose a Template'), { target: { value: '4' } });
    fireEvent.change(screen.getByPlaceholderText('Score (1-10)'), { target: { value: '8' } });
    fireEvent.change(screen.getByPlaceholderText('Add comments / observation details'), { target: { value: 'Good technique' } });
    fireEvent.change(screen.getByPlaceholderText('Your reflection on this rotation period...'), { target: { value: 'Learned a lot' } });
    fireEvent.click(screen.getByRole('button', { name: 'Save Draft' }));
    await waitFor(() => expect(api.createEvaluationSubmission).toHaveBeenCalledWith(expect.objectContaining({ template: 4, resident_comments: 'Learned a lot', responses: [{ field_key: 'score', field_label: 'Score', field_type: 'number', value_text: '', value_number: 8, value_json: {} }, { field_key: 'feedback', field_label: 'Feedback', field_type: 'text', value_text: 'Good technique', value_number: null, value_json: {} }] })));
    expect(api.submitEvaluation).not.toHaveBeenCalled();
    expect(await screen.findByText('Evaluation draft saved.')).toBeInTheDocument();
  });

  it('reports backend authoring failures without navigation', async () => {
    api.createEvaluationSubmission.mockRejectedValueOnce({ response: { data: { detail: 'Period is closed' } } });
    render(<NewEvaluationPage />);
    await screen.findByRole('option', { name: /Mini CEX/ });
    fireEvent.change(screen.getByDisplayValue('Choose a Template'), { target: { value: '4' } });
    fireEvent.click(screen.getByRole('button', { name: 'Submit to Supervisor' }));
    await screen.findByText('Period is closed');
    expect(push).not.toHaveBeenCalled();
  });
});
