# Circular Enabler Category 5 – SPARQL Queries

All queries assume the [common prefixes](index.md#prefixes) are declared.
---

## CQ-CE-12-1

**Who/what actor is responsible for what part of the processes?**

```sparql
SELECT ?role ?actor ?process
WHERE{
    ?participation actorODP:participantRole ?role.
    ?participation actorODP:participatingActor ?actor.
    ?participation actorODP:participationIn ?process.
}
```

---

## CQ-CE-12-2

**What capabillity (e.g. competence) is needed from an actor?**

- **Same as:** [CQ-CE-10-1.sparql](../sparql/cec4.md#cq-ce-10-1)

---

## CQ-CE-12-3

**What is the contingency plan/other possibilities for replacing a material flow in a process?**

---

## CQ-CE-12-4

**Where does this material/component/product come from (source, supplier)?**

```sparql
SELECT ?s ?p ?o WHERE {?s ?p ?o} LIMIT 10
```

---

## CQ-CE-12-5

**Where does the energy needed for a certain process come from (source, supplier)?**

---

## CQ-CE-12-6

**What is the contingency plan/other options for replacing that source of energy?**

---

## CQ-CE-12-7

**What is the best option for energy replacement in this case?**

---

## CQ-CE-12-8

**What is the objective/vision of this circular value network?**

- **Same as:** [CQ-CE-5-17.sparql](../sparql/cec2.md#cq-ce-5-17)

---

## CQ-CE-12-9

**What are the objectives of the actors involved in the network and how are they related to the overall objective/vision?**

---

## CQ-CE-12-10

**What are the obligations and responsibilities of this actor in this collaboration (e.g. circular value network)?**

```sparql
SELECT ?role ?collaboration
WHERE{
    ?participation actorODP:participantRole ?role.
    ?participation actorODP:participatingActor ?actor.
    ?participation actorODP:participationIn ?collaboration.
}
```

---

## CQ-CE-12-11

**Have the obligations and responsibilities been met?**

---

## CQ-CE-13-1

**Who/what actor is responsible for this information?**

---

## CQ-CE-13-2

**What is the history of changes of this information?**

---

## CQ-CE-13-3

**Who has access to this information?**

---

## CQ-CE-13-4

**Who has accessed this information?**

---

## CQ-CE-13-5

**What standard/metadata stardard/format is used for the material data?**

---

## CQ-CE-13-6

**How was this created value verified/is it verified?**

---
