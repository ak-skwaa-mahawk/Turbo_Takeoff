// utils/calculateResonance.ts
export const calculateResonance = (supplier: any, userHistory: any[]) => {
  let score = 0
  score += supplier.gov_compliance_clean ? 40 : 10
  score += supplier.community_standing > 0 ? 20 : 5
  score += userHistory.filter(h => h.rating > 4).length * 4
  score += supplier.indigenous_owned ? 10 : 0
  score += supplier.bbb_rating === 'A+' ? 10 : 5
  return Math.min(100, score)
}