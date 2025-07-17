---
date: 2025-07-16
title: Pairing with AI to Design This Website Part 01 - First Steps
tags:
- tech
- web-development
- ai
- software
- engineering

---
## Everything Begins with an Idea

I'm a bit of a low-profile person on the Internet, which seems to be bad for your career these days, so after 15+ years without having a personal website or blog I decided that it was time to have one again. It does not help that social networks are in a bad shape in 2025, so having my own place to share some ideas and updates does not hurt either, so I started to build one.

I had a few initial requirements, the first one being: I use [Obsidian](https://obsidian.md/) for my notes and would like to publish some of my Obsidian content into my website. I could use [Obsidian Sync](https://obsidian.md/sync) for that, but being in Brazil, adding expenses in USD to my budget is often a no-no. Besides, I wanted to have a bit of personality built into this, so I wanted a Static Site Generator to help me build the way I wanted. Having had some previous experience with [Hugo](https://gohugo.io/) a long time ago, I went wit it. Chose a [nice feature-rich theme](https://blowfish.page/) and fired VS Code.

Then I froze.

I'm a backend-devops-infra-data guy, and I haven't played with frontend code for a long, long time. I used to write a lot of HTML and CSS when [JQuery](https://jquery.com/) and [Lodash](https://lodash.com/) were the gold standard, but opening my theme's code felt completely alien to me. I'm sure there must be a reason why frontend folks love [TailwindCSS](https://tailwindcss.com/), but to my unaccustomed eyes that felt too big a grammar to learn just to put a website up. There was no way I was going to understand this just to build a blog:

```html
<select id="sort-select" class="ml-2 px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent">
...
</select>
```

Then it came to me: _I'm going to AI the shit out of this._

I've been very slow to jump into the AI hype, as I do with most hype. After the first year or so of revolutionary claims and heated politics, the actual decent use cases started to emerge and I started to get curious about it. I tried generating some code here and there and found it to be lacking a bit compared to my own code skills - but here we are, faced with code I suck at writing, so why not give it a chance?

So here we are. My very first article series in this website will be my attempt to log my process pairing with an AI to build this very website you're hopefully reading this article on the future. By process I mean obviously the successes and frustrations, and if the frustrations outweigh the successes too much there's a very real chance you'll never get to read this and I'm just talking to myself as usual.

## Setting up

I already had a stack to work on: **Hugo** to generate a static website and **Obsidian** as my main editor, so **Markdown** would be my content format of choice. I chose [Cursor](https://cursor.com/)as my editor and would leverage my Python background to write the code I needed to feed Hugo with stuff.

First step, let's bring some Obsidian stuff into Hugo. I started writing a simple script to copy Obsidian Markdown files to my Hugo content directory, but this needed a bit of translation. Nothing complicated, but a bit boring, so I invited Cursor's agent for a chat and asked it to do it (sorry, I lost that prompt, it was before I thought about making this into a blog post) and it came up with [this script](https://github.com/guhcampos/guhcampos.github.io/blob/ab861cf75d9ae3025d6d66da1c33d4aaee21e108/scripts/sync-obsidian)

As many before me, I got a little offended by its eagerness to over-explain every line of code:

```python
def process_file(file_path: Path):
    """Process a single markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter, content = extract_frontmatter(content)

    # Skip if not marked for publishing
    if not frontmatter.get('publish', False):
        return

    # Convert content
    content = convert_obsidian_links(content)

    # Determine the section
    section = determine_section(file_path)

    # Clean up the title
    title = frontmatter.get('title', clean_title(file_path.stem))

    # Prepare Hugo frontmatter
    hugo_frontmatter = {
        'title': title,
        'date': frontmatter.get('date', datetime.now().strftime('%Y-%m-%d')),
        'lastmod': datetime.now().strftime('%Y-%m-%d'),
        'draft': False
    }
    ...
```

The whole code is a bit too verbose to my taste, and not very well structured, but it did split the code into functions that made sense, and most importantly: **it worked** the first time. Kudos for my new AI pair!

I wanted to make this repository public as a way to showcase my interactions with the AI, so I made sure to scrub any secret information from it. That of course meant my Obsidian content could not live in the same repository as my website. I already used the great [Obsidian Git](https://github.com/Vinzent03/obsidian-git)to backup my vault to a private Github repository, so why not leverage that?

I then asked the AI to create a Github Actions pipeline to fetch the vault data on build time, directly from the repo, and to my actual surprise, the [generated workflow](https://github.com/guhcampos/guhcampos.github.io/blob/ab861cf75d9ae3025d6d66da1c33d4aaee21e108/.github/workflows/hugo.yml) also did work pretty much the first time. But then the first concerns started. Let's take this snippet as an example:

```yaml
      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: '0.147.7'
          extended: true
```

The AI has added a third party Github action into my pipeline, which begs the question: should I trust it? A well informed developer must be aware of [Supply Chain Attacks](https://www.cloudflare.com/learning/security/what-is-a-supply-chain-attack/) and this is screaming Supply Chain attack to me. Who is [peaceiris](https://github.com/peaceiris)? Is that a trusted developer? Is that even a person or a company? What happens if they decide to add malicious code to this action and send all my precious Obsidian Vault data to some third party?

## Learning a Bunch of Lessons in a Short Time

Ok, time to stop for a second and evaluate options. **First lesson learned: don't trust AI generated code without a very broad and well informed code review**. (that should probably become its own blog article!)

So I did we all technologists do and did a bit of due diligence. Seems like [peaceiris/actions-hugo](https://github.com/peaceiris/actions-hugo)is quite widely used, and has been [consistently releasing trustworthy code](https://github.blog/developer-skills/github/github-action-hero-shohei-ueda/) for six years. It would be quite a bit of work to write my own Github Action for this simple use case, so I decided to trust this and go with the AI generated code. **Ship It!**

But wait, during my due diligence I noted something interesting. Note how the generated code uses `actions-hugo@v2`? Well, this is June 2025 and `actions-hugo@v3` seems to have been released in [April 2024](https://github.com/peaceiris/actions-hugo/releases/tag/v3.0.0) we're over a year out of date from their latest version! Whatever data this model (I think this was `claude-4-sonnet`) was trained on was really, really old. So let's bump this to `v3` before we use it in the real world, shall we?

**Second lesson learned: AI models are trained on data from the past, so take that into account when doing your code review and make sure dependencies and syntax are up to date**

Finally, I was getting uncomfortable with the code quality in this Python script. I have big plans for it besides just copying my Obsidian content into Hugo, so it needed a bit more structure to grow, so I jumped in and refactored it all into a [Click](https://click.palletsprojects.com/en/stable/) tool I could then easily extend beyond its initial abilities. In the meantime, I got to read and understand the code generated by the AI and make some optimizations. All said and done, I think I spent about the same time writing as I would have if starting from scratch, but with a big, big difference: I actually wrote it, while otherwise _I would have actually procrastinated the moment I froze looking at the TailwindCSS code_.

Notice how I didn't even mention the frontend code in this post? I didn't have to do much to put a [basic placeholder homepage](https://blowfish.page/docs/homepage-layout/) up. So I didn't really need the AI for that, but having it made me go **from zero to something** really, really fast, and that gave me traction to actually continue on my journey, overcoming the frustration of hitting an initial wall. **Third lesson learned: AI coding is great for prototyping and putting something out there, even if it's not the definitive version you want to stick to**

I think 3 is a good short number to start with. Three lessons learned in a day of play, so three lessons passed forward with this little blog post. Until next time!