export function formatDate(value) {
  if (!value) {
    return '-'
  }
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date(value))
}

export function formatDateTime(value) {
  if (!value) {
    return '-'
  }
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
}

export function formatCurrency(value) {
  const amount = Number(value || 0)
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    maximumFractionDigits: 0,
  }).format(amount)
}

export function resolveScoreTag(score) {
  if (score >= 90) return 'success'
  if (score >= 80) return ''
  if (score >= 70) return 'warning'
  return 'danger'
}

export function resolveProjectTag(status) {
  return (
    {
      planned: 'info',
      active: 'success',
      paused: 'warning',
      completed: '',
    }[status] || 'info'
  )
}

export function resolveLeaveTag(status) {
  return (
    {
      pending: 'warning',
      approved: 'success',
      rejected: 'danger',
    }[status] || 'info'
  )
}
