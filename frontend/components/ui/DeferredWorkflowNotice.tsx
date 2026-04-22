import PageHeader from './PageHeader';

export default function DeferredWorkflowNotice({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <div className="pg-page">
      <PageHeader title={title} description={description} />
      <section className="pg-card">
        <h2 className="text-lg font-semibold text-gray-900 mb-2">Deferred workflow</h2>
        <p className="text-sm text-gray-600">
          This workflow is implemented outside the current active release gate and is intentionally unavailable in
          the pilot-active navigation. It will be promoted only after its inactive-depth verification passes.
        </p>
      </section>
    </div>
  );
}
