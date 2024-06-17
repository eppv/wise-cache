from typing import List, Optional
from .user import User
from .project import Project
from .mixins import TimestampMixin

dttm_format = '%Y-%m-%dT%H:%M:%S.%fZ'


class GenericArticle(object):
    def __init__(self, attributes_dict: Optional[dict] = None, **kwargs):
        if attributes_dict is None:
            self.__dict__.update(kwargs)
        else:
            if isinstance(attributes_dict, dict):
                self.__dict__.update(attributes_dict)
            else:
                raise TypeError("attributes_dict must be a dictionary")

    def __str__(self):
        return str(self.__dict__)


class Article(TimestampMixin):

    def __init__(self,
                 id: str,
                 attachments: Optional[List['ArticleAttachment']] = None,
                 childArticles: Optional[List['Article']] = None,
                 comments: Optional[List['ArticleComment']] = None,
                 content: Optional[str] = None,
                 created: Optional[int] = None,
                 externalArticle: Optional['ExternalArticle'] = None,
                 hasChildren: bool = False,
                 hasStar: bool = False,
                 idReadable: str = None,
                 ordinal: int = None,
                 parentArticle: Optional[dict] = None,
                 pinnedComments: Optional[List['ArticleComment']] = None,
                 project: Optional[dict] = None,
                 reporter: Optional[dict] = None,
                 summary: Optional[str] = None,
                 tags: Optional[List[dict]] = None,
                 updated: int = None,
                 updatedBy: Optional[dict] = None,
                 visibility: Optional[str] = None,
                 # **kwargs
                 ):
        super().__init__(created=created, updated=updated)
        self._id = id
        self.attachments = attachments if attachments is not None else []
        self.child_articles = childArticles if childArticles is not None else []
        self.comments = comments if comments is not None else []
        self.content = content
        self._external_article = externalArticle
        self._has_children = hasChildren
        self.has_star = hasStar
        self._id_readable = idReadable
        self._ordinal = ordinal
        self.parent_article = Article(**parentArticle) if parentArticle else None
        self._pinned_comments = pinnedComments if pinnedComments is not None else []
        self._project = Project(**project)
        self.reporter = User(**reporter) if reporter is not None else None
        self.summary = summary
        self.tags = [tag['name'] for tag in tags] if tags is not None else []
        self._updated_by = User(**updatedBy) if updatedBy is not None else None
        self.visibility = visibility

    @property
    def id(self) -> str:
        """The ID of the article. Read-only."""
        return self._id

    @property
    def external_article(self) -> Optional['ExternalArticle']:
        """The reference to the article or a similar object in the originating third-party system. Read-only. Can be null."""
        return self._external_article

    @property
    def has_children(self) -> bool:
        """When true, the article has sub-articles. Read-only."""
        return self._has_children

    @property
    def id_readable(self) -> str:
        """The article ID. Read-only."""
        return self._id_readable

    @property
    def ordinal(self) -> int:
        """The position of the article in the tree. Read-only."""
        return self._ordinal

    @property
    def pinned_comments(self) -> List['ArticleComment']:
        """The list of comments that are pinned in the article. Read-only."""
        return self._pinned_comments

    @property
    def project(self) -> Optional['Project']:
        """The project where the article belongs. Read-only."""
        return self._project

    @property
    def updated_by(self) -> Optional['User']:
        """The user who last updated the article. Read-only. Can be null."""
        return self._updated_by

    def __str__(self):
        return (
            f"Article(id='{self.id}', "
            f"idReadable='{self.id_readable}', "
            f"summary='{self.summary}', "
            f"created={self.created}, "
            f"updated={self.updated}, "
            f"hasChildren={self.has_children}, "
            f"hasStar={self.has_star}, "
            f"tags={self.tags}, "
            f"project='{self.project}', "
            f"reporter='{self.reporter.name}', "
            f"updatedBy='{self.updated_by.name}', "
            f"visibility='{self.visibility}')"
        )


class ArticleAttachment:
    def __init__(self,
                 id: str,
                 name: Optional[str] = None,
                 author: Optional['User'] = None,
                 created: int = None,
                 updated: int = None,
                 size: int = None,
                 extension: Optional[str] = None,
                 charset: Optional[str] = None,
                 mime_type: Optional[str] = None,
                 meta_data: Optional[str] = None,
                 draft: bool = False,
                 removed: bool = False,
                 base64_content: Optional[str] = None,
                 url: Optional[str] = None,
                 visibility: Optional[str] = None,
                 article: Optional['Article'] = None,
                 comment: Optional['ArticleComment'] = None):
        self._id = id
        self.name = name
        self._author = author
        self._created = created
        self._updated = updated
        self._size = size
        self._extension = extension
        self._charset = charset
        self._mimeType = mime_type
        self._metaData = meta_data
        self._draft = draft
        self._removed = removed
        self.base64Content = base64_content
        self._url = url
        self.visibility = visibility
        self._article = article
        self._comment = comment

    @property
    def id(self) -> str:
        """The ID of the article attachment. Read-only."""
        return self._id

    @property
    def author(self) -> Optional['User']:
        """The user who attached the file to the article. Read-only. Can be null."""
        return self._author

    @property
    def created(self) -> int:
        """The timestamp in milliseconds indicating the moment when the attachment was created. Stored as a unix timestamp at UTC. Read-only."""
        return self._created

    @property
    def updated(self) -> int:
        """The timestamp in milliseconds indicating the last update of the attachment. Stored as a unix timestamp at UTC. Read-only."""
        return self._updated

    @property
    def size(self) -> int:
        """The size of the attached file in bytes. Read-only."""
        return self._size

    @property
    def extension(self) -> Optional[str]:
        """The extension that defines the file type. Read-only. Can be null."""
        return self._extension

    @property
    def charset(self) -> Optional[str]:
        """The charset of the file. Read-only. Can be null."""
        return self._charset

    @property
    def mimeType(self) -> Optional[str]:
        """The MIME type of the file. Read-only. Can be null."""
        return self._mimeType

    @property
    def metaData(self) -> Optional[str]:
        """The dimensions of an image file. For an image file, the value is rw=&rh=. For a non-image file, the value is empty. Read-only. Can be null."""
        return self._metaData

    @property
    def draft(self) -> bool:
        """If true, the attachment is not yet published, otherwise false. Read-only."""
        return self._draft

    @property
    def removed(self) -> bool:
        """If true, the attachment is considered to be removed. Read-only."""
        return self._removed

    @property
    def url(self) -> Optional[str]:
        """The URL of the file. Read-only. Can be null."""
        return self._url

    @property
    def article(self) -> Optional['Article']:
        """The article that the file is attached to. Read-only. Can be null."""
        return self._article

    @property
    def comment(self) -> Optional['ArticleComment']:
        """The comment that the file is attached to. Returns null if the file was attached directly to the article. Read-only."""
        return self._comment


class ArticleComment:
    def __init__(self,
                 id: str,
                 article: Optional['Article'] = None,
                 attachments: Optional[List['ArticleAttachment']] = None,
                 author: Optional['User'] = None,
                 created: int = None,
                 pinned: bool = False,
                 reactions: Optional[List[str]] = None,
                 text: Optional[str] = None,
                 updated: int = None,
                 visibility: Optional[str] = None):
        self._id = id
        self._article = article
        self.attachments = attachments if attachments is not None else []
        self._author = author
        self._created = created
        self.pinned = pinned
        self.reactions = reactions if reactions is not None else []
        self.text = text
        self._updated = updated
        self.visibility = visibility

    @property
    def id(self) -> str:
        """The ID of the article comment. Read-only."""
        return self._id

    @property
    def article(self) -> Optional['Article']:
        """The article the comment belongs to. Read-only. Can be null."""
        return self._article

    @property
    def author(self) -> Optional['User']:
        """The user who created the comment. Read-only. Can be null."""
        return self._author

    @property
    def created(self) -> int:
        """The timestamp in milliseconds indicating the moment when the comment was posted. Stored as a unix timestamp at UTC. Read-only."""
        return self._created

    @property
    def updated(self) -> int:
        """The timestamp in milliseconds indicating the last update of the comment. Stored as a unix timestamp at UTC. Read-only."""
        return self._updated


class ExternalArticle:
    def __init__(self,
                 id: str,
                 attachments: Optional[List[ArticleAttachment]] = None,
                 content: Optional[str] = None,
                 reporter: Optional[User] = None,
                 summary: Optional[str] = None,
                 visibility: Optional[str] = None):
        self._id = id
        self.attachments = attachments if attachments is not None else []
        self.content = content
        self.reporter = reporter
        self.summary = summary
        self.visibility = visibility

    @property
    def id(self) -> str:
        return self._id
