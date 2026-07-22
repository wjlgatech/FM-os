reverse-engineered text (<inline>) → blueprint  [evidence 0/100, best of 3]
  1. Fetch the raw content from https://www.nomadicai.com
       when: Network access to the target URL is available
       then: The raw HTML/text of the page is retrieved and stored locally
  2. Parse the retrieved content to isolate the text artifact
       when: Raw page content has been fetched
       then: The relevant text elements are extracted and separated from markup
  3. Normalize and structure the extracted text
       when: Text elements have been isolated from the parsed content
       then: The text is cleaned, ordered, and organized into a coherent structure
  4. Reproduce the text artifact in the desired output format
       when: Normalized and structured text is ready
       then: A faithful reproduction of the text artifact is produced
  5. Verify the reproduction against the source
       when: The reproduced text artifact exists
       then: The reproduction is confirmed to accurately match the original source content
  fidelity: ✗ unsupported — 0/100 via evidence gate (text-evidence overlap — a readable model, not a reproduction)
  method (spine): structure + rules extraction from a rendered document [30y · load-bearing] — https://en.wikipedia.org/wiki/Reverse_engineering
