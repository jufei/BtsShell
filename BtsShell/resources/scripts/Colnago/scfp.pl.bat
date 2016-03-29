@rem= 'Read this as an array assignment
@ECHO OFF
goto begin_perl_code
@rem ';
#
######################################################################
#!/usr/bin/perl
#
# Author: Christian Huesch (GPPAG) , May 2010
#
# Sort the objects of an xml like structure.
# Program takes the data from the file or stdin
# and prints the result to stdout, like cat.
#
# Attention: This script doesnt check the xml syntax, but
#            assums the syntax is ok.
#            Usage at own risk.
#
# Always Have Fun :-)
#
# main changes:
#   Sep 2010: (CH) sort equal items by the first difference of their sorted content
#                  calculated by expensive subtreepseudovalue(\$)

use strict ;
use English ;

my $ref_scf ;

# the hash structure that will be build by buildtree reading the input
#
# value = \(
#   head    => $info      # all text from beginning upto values
#   nosort  => $nosort    # values shall not be sorted if set (not needed yet)
#   subvals => @values    # list of recurive sub objects
#   simple  => $data      # string/value not enclosed in any sub structure
#   foot    => $closing   # all text after the values to end of structure
# )
#

sub buildtree {
    my %oh = ();
    my $head;
    if (length == 0) { $_ = <> } ;
    while(! eof) {
        s/^\s+//gs;
        if( m(^<!--) ) {  # eat all comments <!-- ... -->
            eatcomment();
        }
        if(m(^<\?.*?\?>)) {  # select if like <?xml version="1.0"?>
            $head = $&;
            $oh{head} = $head;
            $_ = $POSTMATCH;
            my @val = ( buildtree() );
            $oh{subvals} = \@val ;
            last;
        }
        if(m(^<(?!/).*?/>)) {  # select if like tag <xxxxx ... />
            $head = $&;
            $oh{head} = $head;
            $_ = $POSTMATCH;
            last;
        }
        if(m(^<(?!/).*?>)) {  # select if like start <xxxxx ... >
            $head = $&;
            $oh{head} = $head;
            $_ = $POSTMATCH;
            getvals($head,\%oh);
            last;
        }
        #readin next
        $_ .= <>;
    }
    return \%oh;
}

sub getvals {
    my ($head,$ref_oh) = @_;
    my ($ftag) = $head =~ /<(\w+)/;
    while(! eof || length) {
        s/^\s+//gs;
        if( m(^<!--) ) {  # eat all comments <!-- ... -->
            eatcomment();
        }
        if ( m(^</$ftag>) ) {  # found end <xxxxx/>
            $ref_oh->{foot} .= $MATCH;
            $_ = $POSTMATCH;
            last;
        }
        if( m(^<(?!/).*?>) ) {  # found start of sub structure <xxxx>
            push @{$ref_oh->{subvals}},buildtree();
            next;
        }
        if ( m((.)(<))s ) {  # found simple text/value
            $ref_oh->{simple} .= $PREMATCH.$1;
            $_ = $2.$POSTMATCH;
            next;
        }
        if ( eof ) {  # reached end unfurtunately => return
            $ref_oh->{simple} .= $_;
            $_ = '';
            last;
        }
        #readin next
        $_ .= <>;
    }
}

sub eatcomment {
    my $comment;
    while ( m(^<!--) ) {
        if ( m(<!--.*-->)s ) {  # readin until comment closed
            $comment = $MATCH;
            $_ = $POSTMATCH;
            last;
        }
        if (eof) {  # reached end unfortunately
            $comment = $_;
            $_ = '';
            last;
        }
        $_ .= <>;
    }
    return $comment;
}

sub printtree {
    my ($indent,$ref_oh) = @_;
    my $i = '  ' x $indent;   # print with indent
    if (   ! defined $ref_oh->{subvals}
         || scalar(@{$ref_oh->{subvals}})==0 ) {  # print simples in one line
        print $i,$ref_oh->{head},
              $ref_oh->{simple},
              $ref_oh->{foot},"\n";
    } else {  # print structure (recursive)
        print $i,$ref_oh->{head},"\n";
        foreach my $ro (@{$ref_oh->{subvals}}) {
            printtree($indent+1,$ro);
        }
        print $i,'  ',$ref_oh->{simple},"\n"  if (defined $ref_oh->{simple});
        print $i,$ref_oh->{foot},"\n";
    }
}

sub subtreepseudovalue {
    my ($ref_s) = @_;
    my $pseudo = '' . $ref_s->{head} . $ref_s->{simple};
    foreach my $rs (@{$ref_s->{subvals}}) {
        $pseudo .= subtreepseudovalue ($rs);
    }
    return $pseudo;
}

sub sorttree {
    my ($ref_oh) = @_;
    if ( defined $ref_oh->{subvals} ) {
        foreach my $ro (@{$ref_oh->{subvals}}) {
            sorttree($ro);
        }
        if ( ! $ref_oh->{nosort} ) {
            # sort alphabetically by starting tag,
            #   prefered by distname if exists
            my @new_subvals = sort {
                       ($a->{head} =~ m((distName=".*?")))[0]
                   cmp ($b->{head} =~ m((distName=".*?")))[0]
                ||      $a->{head}
                   cmp  $b->{head}
                ||      subtreepseudovalue($a)
                   cmp  subtreepseudovalue($b)
            } @{$ref_oh->{subvals}} ;
            $ref_oh->{subvals} = \@new_subvals;
        }
    }
}


$ref_scf = buildtree();

sorttree ($ref_scf);

printtree (0,$ref_scf);

#
######################################################################
#
exit 0;

__END__
:begin_perl_code
IF EXIST %0 perl %0 %1 > %1.sorted.xml
IF EXIST %0.bat perl %0.bat %1 > %1.sorted.xml
rem pause

rem # vim:ts=4:sw=4:et:ai
