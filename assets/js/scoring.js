/**
 * Identification scoring — the one piece of logic in the wizard that is worth
 * testing on its own. Loaded in the browser as a global (GLSscore) and in Node
 * as a CommonJS module, so `npm test` runs the same code the page runs.
 */
(function (root, factory) {
  var api = factory();
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.GLSscore = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  /**
   * Sum the points each answered option awards.
   * @param {Array} answers  one entry per question: { id, label, add: { familyId: points } }
   * @returns {Object} familyId -> total points
   */
  function tally(answers) {
    var scores = {};
    (answers || []).forEach(function (answer) {
      if (!answer || !answer.add) return;
      Object.keys(answer.add).forEach(function (familyId) {
        var points = answer.add[familyId];
        if (typeof points === 'number' && points > 0) {
          scores[familyId] = (scores[familyId] || 0) + points;
        }
      });
    });
    return scores;
  }

  /**
   * Rank catalog entries by score.
   * Ties are broken by catalog order so the result is deterministic — two runs of
   * the wizard must not give different answers for the same inputs.
   * @returns {Array} [{ id, score, family }] highest first, zero-score entries dropped
   */
  function rank(answers, catalog) {
    var scores = tally(answers);
    return (catalog || [])
      .map(function (family, index) {
        return { id: family.id, score: scores[family.id] || 0, family: family, order: index };
      })
      .filter(function (entry) { return entry.score > 0; })
      .sort(function (a, b) { return b.score - a.score || a.order - b.order; });
  }

  /**
   * Build the answer objects the wizard passes to rank(), given a list of
   * question ids and chosen option ids. Returns null if any choice is invalid,
   * so a caller cannot silently score a nonexistent option.
   */
  function answersFrom(questions, choices) {
    var out = [];
    for (var i = 0; i < questions.length; i++) {
      var wanted = choices[questions[i].id];
      if (wanted === undefined || wanted === null) return null;
      var option = (questions[i].options || []).filter(function (o) { return o.id === wanted; })[0];
      if (!option) return null;
      out.push({ id: option.id, label: option.label, add: option.add || {} });
    }
    return out;
  }

  /**
   * Decide what to actually tell the user.
   *
   * A ranked list alone is not enough: a 3-way tie on two points each is not an
   * identification, and presenting the first entry as "most likely" would be a
   * confident-looking guess. Below MIN_CONFIDENT_SCORE, or when the top score is
   * shared, the wizard says so instead of picking a winner.
   */
  var MIN_CONFIDENT_SCORE = 5;

  function decide(answers, catalog) {
    var ranked = rank(answers, catalog);
    if (!ranked.length) {
      return { confident: false, top: null, tied: [], ranked: ranked, reason: 'no-match' };
    }
    var topScore = ranked[0].score;
    var tied = ranked.filter(function (entry) { return entry.score === topScore; });
    if (topScore < MIN_CONFIDENT_SCORE) {
      return { confident: false, top: null, tied: tied, ranked: ranked, reason: 'too-weak' };
    }
    if (tied.length > 1) {
      return { confident: false, top: null, tied: tied, ranked: ranked, reason: 'tied' };
    }
    return { confident: true, top: ranked[0], tied: tied, ranked: ranked, reason: 'ok' };
  }

  return {
    tally: tally,
    rank: rank,
    answersFrom: answersFrom,
    decide: decide,
    MIN_CONFIDENT_SCORE: MIN_CONFIDENT_SCORE
  };
});
